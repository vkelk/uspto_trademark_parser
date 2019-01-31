"""
__version__ = '1.2.0'
__date__ = '2018-11-08'
"""

import argparse
import concurrent.futures as cf
from datetime import datetime
import logging
import logging.config
import os
from pprint import pprint
import re
import requests
import sys
import time
import zipfile

from lxml import etree, html

from db_pgsql import Db
from helpers import download_html, get_text_or_none

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
WORK_DIR = os.path.join(BASE_DIR, 'work_dir')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
MAIN_URL = 'https://bulkdata.uspto.gov/data/trademark/dailyxml/applications/'


def print_dict(dictionary):
    for k, v in dictionary.items():
        print(k, type(v), v)


def parse_case(case, doc_id, file_id, dbc):
    def parse_case_files():
        case_files = {'serial_number': doc_id,
                      'file_id': file_id,
                      'registration_number': get_text_or_none(case, 'registration-number/text()'),
                      'transaction_date': get_text_or_none(case, 'transaction-date/text()')}
        return dbc.insert_dict(case_files, 'trademark_app_case_files')

    def parse_headers():
        case_file_headers = {'serial_number': doc_id}
        case_file_header_items = (
            'filing_date', 'status_code', 'status_date', 'mark_identification', 'mark_drawing_code',
            'attorney_docket_number', 'attorney_name', 'principal_register_amended_in',
            'supplemental_register_amended_in', 'trademark_in', 'collective_trademark_in', 'service_mark_in',
            'collective_service_mark_in', 'collective_membership_mark_in', 'certification_mark_in',
            'cancellation_pending_in', 'published_concurrent_in', 'concurrent_use_in',
            'concurrent_use_proceeding_in', 'interference_pending_in', 'opposition_pending_in', 'section_12c_in',
            'section_2f_in', 'section_2f_in_part_in', 'renewal_filed_in', 'section_8_filed_in',
            'section_8_partial_accept_in', 'section_8_accepted_in', 'section_15_acknowledged_in',
            'section_15_filed_in', 'supplemental_register_in', 'foreign_priority_in', 'change_registration_in',
            'intent_to_use_in', 'intent_to_use_current_in', 'filed_as_use_application_in',
            'amended_to_use_application_in', 'use_application_currently_in', 'amended_to_itu_application_in',
            'filing_basis_filed_as_44d_in', 'amended_to_44d_application_in', 'filing_basis_current_44d_in',
            'filing_basis_filed_as_44e_in', 'filing_basis_current_44e_in', 'amended_to_44e_application_in',
            'without_basis_currently_in', 'filing_current_no_basis_in', 'color_drawing_filed_in',
            'color_drawing_current_in', 'drawing_3d_filed_in', 'drawing_3d_current_in',
            'standard_characters_claimed_in', 'filing_basis_filed_as_66a_in', 'filing_basis_current_66a_in',
            'current_location', 'location_date', 'employee_name', 'registration_date',
            'published_for_opposition_date', 'amend_to_register_date', 'abandonment_date', 'cancellation_code',
            'cancellation_date', 'republished_12c_date', 'domestic_representative_name', 'renewal_date',
            'law_office_assigned_location_code')
        for hitem in case_file_header_items:
            search_term = 'case-file-header/' + hitem.replace('_', '-') + '/text()'
            case_file_headers[hitem] = get_text_or_none(case, search_term)
        return dbc.insert_dict(case_file_headers, 'trademark_app_case_file_headers')

    def parse_statements():
        cfs_elements = case.findall('case-file-statements/case-file-statement')
        lst = []
        for child in cfs_elements:
            case_file_statements = {'serial_number': doc_id,
                                    'type_code': get_text_or_none(child, 'type-code/text()'),
                                    'text': get_text_or_none(child, 'text/text()')}
            lst.append(case_file_statements)
        dbc.insert_listdict(lst, 'trademark_app_case_file_statements')

    def parse_event_statements():
        cfes_elements = case.findall('case-file-event-statements/case-file-event-statement')
        lst = []
        for child in cfes_elements:
            case_file_event_statements = {'serial_number': doc_id,
                                          'code': get_text_or_none(child, 'code/text()'),
                                          'type': get_text_or_none(child, 'type/text()'),
                                          'description_text': get_text_or_none(child, 'description-text/text()'),
                                          'date': get_text_or_none(child, 'date/text()'),
                                          'number': get_text_or_none(child, 'number/text()')}
            lst.append(case_file_event_statements)
        dbc.insert_listdict(lst, 'trademark_app_case_file_event_statements')

    def parse_prior_registration_applications():
        pra_elements = case.findall('prior-registration-applications/prior-registration-application')
        other_related_in = get_text_or_none(case, 'prior-registration-applications/other-related-in/text()')
        lst = []
        for child in pra_elements:
            prior_registration_applications = {'serial_number': doc_id,
                                               'other_related_in': other_related_in,
                                               'relationship_type': get_text_or_none(child,
                                                                                     'relationship-type/text()'),
                                               'number': get_text_or_none(child, 'number/text()')}
            lst.append(prior_registration_applications)
        dbc.insert_listdict(lst, 'trademark_app_prior_registration_applications')

    def parse_foreign_applications():
        fa_elements = case.findall('foreign-applications/foreign-application')
        lst = []
        for child in fa_elements:
            foreign_applications = {'serial_number': doc_id}
            foreign_applications_items = (
                'filing_date', 'registration_date', 'registration_expiration_date', 'registration_renewal_date',
                'registration_renewal_expiration_date', 'entry_number', 'application_number', 'country',
                'other', 'registration_number', 'renewal_number', 'foreign_priority_claim_in')
            for hitem in foreign_applications_items:
                search_term = hitem.replace('_', '-') + '/text()'
                foreign_applications[hitem] = get_text_or_none(child, search_term)
            lst.append(foreign_applications)
        dbc.insert_listdict(lst, 'trademark_app_foreign_applications')

    def parse_classifications():
        classification_elements = case.findall('classifications/classification')
        for child in classification_elements:
            classifications = {'serial_number': doc_id}
            classifications_items = (
                'international_code_total_no', 'us_code_total_no', 'international_code', 'status_code',
                'status_date', 'first_use_anywhere_date', 'first_use_in_commerce_date', 'primary_code')
            for hitem in classifications_items:
                search_term = hitem.replace('_', '-') + '/text()'
                classifications[hitem] = get_text_or_none(child, search_term)
            classification_id = dbc.insert_dict(classifications, 'trademark_app_classifications')
            code_elements = child.findall('us-code')
            lst = []
            for subchild in code_elements:
                case_file_us_codes = {'serial_number': doc_id,
                                      'classification_id': classification_id,
                                      'us_code': subchild.text}
                lst.append(case_file_us_codes)
            dbc.insert_listdict(lst, 'trademark_app_us_codes')

    def parse_correspondents():
        correspondent_elements = case.findall('correspondent')
        lst = []
        for child in correspondent_elements:
            case_file_correspondent = {'serial_number': doc_id}
            case_file_correspondent_items = (
                'address_1', 'address_2', 'address_3', 'address_4', 'address_5')
            for hitem in case_file_correspondent_items:
                search_term = hitem.replace('_', '-') + '/text()'
                case_file_correspondent[hitem] = get_text_or_none(child, search_term)
            lst.append(case_file_correspondent)
        dbc.insert_listdict(lst, 'trademark_app_correspondents')

    def parse_owners():
        cfo_elements = case.findall('case-file-owners/case-file-owner')
        lst = []
        for child in cfo_elements:
            case_file_owners = {'serial_number': doc_id}
            case_file_owners_items = (
                'entry_number', 'party_type', 'legal_entity_type_code', 'entity_statement', 'party_name',
                'address_1', 'address_2', 'city', 'state', 'country', 'other', 'postcode', 'dba_aka_text',
                'composed_of_statement', 'name_change_explanation')
            for hitem in case_file_owners_items:
                search_term = hitem.replace('_', '-') + '/text()'
                case_file_owners[hitem] = get_text_or_none(child, search_term)
            case_file_owners['nationality'] = get_text_or_none(child, 'nationality/country/text()')
            lst.append(case_file_owners)
        dbc.insert_listdict(lst, 'trademark_app_case_file_owners')

    def parse_design_searches():
        cfds_elements = case.findall('design-searches/design-search')
        lst = []
        for child in cfds_elements:
            case_file_design_searches = {'serial_number': doc_id,
                                         'code': get_text_or_none(child, 'code/text()')}
            lst.append(case_file_design_searches)
        dbc.insert_listdict(lst, 'trademark_app_design_searches')

    def parse_international_registration():
        cfir_elements = case.findall('international-registration')
        lst = []
        for child in cfir_elements:
            case_file_international_registration = {'serial_number': doc_id}
            case_file_international_registration_items = (
                'international_registration_number', 'international_registration_date',
                'international_publication_date', 'international_renewal_date', 'auto_protection_date',
                'international_death_date', 'international_status_code', 'international_status_date',
                'priority_claimed_in', 'priority_claimed_date', 'first_refusal_in')
            for hitem in case_file_international_registration_items:
                search_term = hitem.replace('_', '-') + '/text()'
                case_file_international_registration[hitem] = get_text_or_none(child, search_term)
            lst.append(case_file_international_registration)
        dbc.insert_listdict(lst, 'trademark_app_international_registration')

    def parse_madrid_international_filing_record():
        mifr_elements = case.findall('madrid-international-filing-requests/madrid-international-filing-record')
        for child in mifr_elements:
            madrid_international_filing_record = {'serial_number': doc_id}
            madrid_international_filing_record_items = (
                'entry_number', 'reference_number', 'original_filing_date_uspto',
                'international_registration_number',
                'international_registration_date', 'international_status_code',
                'international_status_date', 'irregularity_reply_by_date', 'international_renewal_date')
            for hitem in madrid_international_filing_record_items:
                search_term = hitem.replace('_', '-') + '/text()'
                madrid_international_filing_record[hitem] = get_text_or_none(child, search_term)
            mifr_id = dbc.insert_dict(madrid_international_filing_record,
                                      'trademark_app_madrid_international_filing_record')
            mhe_elements = child.findall('madrid-history-events/madrid-history-event')
            lst = []
            for subchild in mhe_elements:
                madrid_history_events = {'serial_number': doc_id,
                                         'madrid_international_filing_record_id': mifr_id}
                madrid_history_events_items = (
                    'code', 'date', 'description_text', 'entry_number')
                for hitem in madrid_history_events_items:
                    search_term = hitem.replace('_', '-') + '/text()'
                    madrid_history_events[hitem] = get_text_or_none(subchild, search_term)
                lst.append(madrid_history_events)
            dbc.insert_listdict(lst, 'trademark_app_madrid_history_events')

    start_time = time.time()
    tm = doc_id
    try:
        parse_case_files()
    except KeyboardInterrupt:
        dbc.cnx.rollback()
        sys.exit()
    except SystemExit:
        dbc.cnx.rollback()
        sys.exit()
    except Exception:
        logger.error('[%s] error while parsing doc_id %s', file_id, doc_id)
        logger.exception('message')
        dbc.cnx.rollback()
        tm = None
    with cf.ThreadPoolExecutor(max_workers=11) as executor:
        try:
            # executor.submit(parse_case_files)
            executor.submit(parse_headers)
            executor.submit(parse_statements)
            executor.submit(parse_event_statements)
            executor.submit(parse_prior_registration_applications)
            executor.submit(parse_foreign_applications)
            executor.submit(parse_classifications)
            executor.submit(parse_correspondents)
            executor.submit(parse_owners)
            executor.submit(parse_design_searches)
            executor.submit(parse_international_registration)
            executor.submit(parse_madrid_international_filing_record)
        except KeyboardInterrupt:
            dbc.cnx.rollback()
            sys.exit()
        except SystemExit:
            dbc.cnx.rollback()
            sys.exit()
        except Exception:
            logger.error('[%s] error while parsing doc_id %s', file_id, doc_id)
            logger.exception('message')
            dbc.cnx.rollback()
            tm = None
    if tm is not None:
        dbc.cnx.commit()
        logger.info(
            '[%s] Inserted tm %s in [%6.3f sec]', file_id, doc_id, time.time() - start_time
            )
    else:
        logger.warning('[%s] Could not insert %s', file_id, doc_id)
        raise

    # dbc.case_file_update_status(doc_id, 'true')
    # dbc.cnx.commit()
    # logger.info('Inserted case %s in [%s sec]', doc_id, time.time() - start_time)


def parse_file(filename, file_id):
    dbc = Db()
    if WORK_DIR not in filename:
        filename = os.path.join(WORK_DIR, filename)
    with open(filename, 'rb') as inputfile:
        file_start_time = time.time()
        logger.info('Parsing file %s' % filename)
        context = etree.iterparse(inputfile, events=('end',), tag='case-file')
        for event, case in context:
            doc_id = int(get_text_or_none(case, 'serial-number/text()'))
            serial_db = dbc.serial_get(doc_id, file_id)
            if serial_db is not None:
                transaction_date_string = get_text_or_none(case, 'transaction-date/text()')
                if transaction_date_string:
                    transaction_date = datetime.strptime(transaction_date_string, '%Y%m%d').date()
                else:
                    logger.warning('Missing transaction date in XML')
                    transaction_date = None
                if serial_db['transaction_date'] is not None and serial_db['transaction_date'] != '':
                    db_transaction_date = datetime.strptime(serial_db['transaction_date'], '%Y%m%d').date()
                else:
                    logger.warning('Missing transaction date in database')
                    db_transaction_date = None
                if transaction_date > db_transaction_date \
                    or (serial_db['status'] is False and args.force) \
                    or (transaction_date > db_transaction_date and args.parseall and args.force):
                    for t in ('trademark_app_case_files', 'trademark_app_case_file_event_statements',
                              'trademark_app_case_file_headers', 'trademark_app_case_file_owners',
                              'trademark_app_case_file_statements', 'trademark_app_classifications',
                              'trademark_app_correspondents', 'trademark_app_design_searches',
                              'trademark_app_foreign_applications', 'trademark_app_international_registration',
                              'trademark_app_madrid_history_events', 'trademark_app_madrid_international_filing_record',
                              'trademark_app_prior_registration_applications', 'trademark_app_us_codes'):
                        dbc.delete_serial(doc_id, t)
                        dbc.cnx.commit()
                    logger.info('[%s] Deleted serial %s from all tables', os.path.basename(filename), doc_id)
                    logger.info('[%s] Processing existing serial number %s', os.path.basename(filename), doc_id)
                    parse_case(case, doc_id, file_id, dbc)
            else:
                logger.info('[%s] Processing new serial number %s', os.path.basename(filename), doc_id)
                parse_case(case, doc_id, file_id, dbc)
            case.clear()
    dbc.file_update_status(file_id, 'finished')
    os.remove(filename)
    logger.info('[%s] Finished parsing file in [%s sec]', os.path.basename(filename), time.time() - file_start_time)


def create_logger():
    date = time.strftime('%Y-%m-%d')
    log_filename = 'tm_parser_' + str(date) + '.log'
    log_file = os.path.join(LOG_DIR, log_filename)
    ini_file = os.path.join(BASE_DIR, 'log.ini')
    # Windows paths hack
    log_file = log_file.replace('\\', '\\\\')
    ini_file = ini_file.replace('\\', '\\\\')
    logging.config.fileConfig(ini_file, defaults={'logfilename': log_file}, disable_existing_loggers=False)
    return logging.getLogger(__name__)


def download_file(url):
    zip_filename = os.path.join(WORK_DIR, url.split('/')[-1])
    if 'apc18840407-' in zip_filename:
        xml_filename = zip_filename.replace('apc18840407-20', 'apc').replace('zip', 'xml')
    else:
        xml_filename = zip_filename.replace('zip', 'xml')
    if os.path.isfile(zip_filename) or os.path.isfile(xml_filename):
        logger.debug('File already exists.')
    else:
        logger.debug('Downloading %s', url)
        # NOTE the stream=True parameter
        logger.debug('Getting zip from %s' % url)
        start_time = time.time()
        r = requests.get(url, stream=True)
        with open(zip_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        r.close()
        logger.info('File %s downloaded in [%s sec].', zip_filename, time.time() - start_time)
    if not os.path.isfile(xml_filename) and os.path.isfile(zip_filename):
        try:
            zip_ref = zipfile.ZipFile(zip_filename, 'r')
            zip_ref.extractall(WORK_DIR)
            zip_ref.close()
            os.remove(zip_filename)
        except Exception:
            logger.error('UNZIP ERROR. Deleting file %s' % zip_filename)
            os.remove(zip_filename)
    logger.info('XMLfilename %s', xml_filename)
    return xml_filename.split('/')[-1]


def get_urls(main_url):
    html_content = download_html(main_url)
    html_tree = html.fromstring(html_content)
    html_tree.make_links_absolute(main_url)
    content = html_tree.xpath('//div[@class="container"]/table[2]//tr')
    files = ()
    for row in content:
        a = row.xpath('td/a[contains(@href, ".zip")]')
        if len(a) > 0:
            apc = {'url': a[0].get('href'),
                   'size': row.xpath('td[2]//text()')[0],
                   'date_string': row.xpath('td[3]//text()')[0]}
            files = (apc,) + files
    if len(files) > 0:
        return sorted(files, key=lambda k: k['date_string'], reverse=True)
    return None


def main_worker(file):
    dbc = Db()
    file_check = dbc.file_check(file)
    if file_check is None:
        xml_filename = download_file(file['url'])
        if xml_filename is not None:
            inserted_id = dbc.file_insert(file, os.path.basename(xml_filename))
            try:
                parse_file(xml_filename, inserted_id)
            except Exception:
                logger.exception('message')
                raise
    elif file_check['status'] in ['new', 'reparsing'] or args.force:
        logger.warning('File %s exists into database. Going to process again', file_check['filename'])
        if not os.path.isfile(os.path.join(WORK_DIR, file_check['filename'])):
            xml_filename = download_file(file['url'])
        else:
            xml_filename = file_check['filename']
        try:
            parse_file(xml_filename, file_check['id'])
        except Exception:
            logger.exception('message')
            raise
    else:
        logger.info('File %s is already inserted into database. Skiping it', file_check['filename'])
        if args.parse:
            logger.info('Nothing to work. Exiting.')
            exit()


def sub_main():
    files_tuple = get_urls(MAIN_URL)
    # single-thread test
    # for file in files_tuple:
    #     main_worker(file)
    # sys.exit()
    with cf.ThreadPoolExecutor(max_workers=12) as executor:
        try:
            executor.map(main_worker, files_tuple)
        except Exception:
            logger.exception('message')


logger = create_logger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Downloads and parses trademarks.')
    parser.add_argument('--parse', help='Parses most recent data.', action="store_true")
    parser.add_argument('--parseall', help='Parses all the data.', action="store_true")
    parser.add_argument('--force', help='Forces to discard old data, use with --parseall command.', action="store_true")
    args = parser.parse_args()
    if args.parse or args.parseall:
        os.makedirs(os.path.dirname(WORK_DIR), exist_ok=True)
        os.makedirs(os.path.dirname(LOG_DIR), exist_ok=True)
        sub_main()
    else:
        parser.print_help()
        sys.exit()
