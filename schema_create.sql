-- trademark_app_case_files definition

CREATE TABLE trademark_app_case_files (
	id bigserial NOT NULL,
	serial_number int8 NOT NULL,
	registration_number varchar(30) NULL DEFAULT NULL::character varying,
	transaction_date varchar(30) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT false,
	file_id int4 NULL,
	CONSTRAINT id PRIMARY KEY (id),
	CONSTRAINT serial_number UNIQUE (serial_number)
);
CREATE INDEX ON trademark_app_case_files USING btree (file_id);
CREATE INDEX ON trademark_app_case_files USING btree (serial_number);


-- trademark_fileinfo definition

CREATE TABLE trademark_fileinfo (
	id bigserial NOT NULL,
	filename varchar(30) NOT NULL,
	filesize int8 NULL,
	created timestamptz NOT NULL DEFAULT now(),
	status varchar(15) NOT NULL DEFAULT 'new'::character varying,
	url varchar(255) NULL,
	date_string date NULL,
	modified timestamptz NOT NULL DEFAULT now(),
	CONSTRAINT trademark_fileinfo_pkey PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ON trademark_fileinfo USING btree (url);
CREATE INDEX ON trademark_fileinfo USING btree (filename);


-- trademark_app_case_file_event_statements definition

CREATE TABLE trademark_app_case_file_event_statements (
	id bigserial NOT NULL,
	serial_number int8 NOT NULL,
	code varchar(30) NULL DEFAULT NULL::character varying,
	"type" varchar(3) NULL DEFAULT NULL::character varying,
	description_text varchar(100) NULL DEFAULT NULL::character varying,
	"date" varchar(20) NULL DEFAULT NULL::character varying,
	"number" varchar(20) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	CONSTRAINT trademark_app_case_file_event_statements_pkey PRIMARY KEY (id),
	CONSTRAINT trademark_app_case_file_event_statements_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_case_file_event_statements USING btree (serial_number);


-- trademark_app_case_file_headers definition

CREATE TABLE trademark_app_case_file_headers (
	id bigserial NOT NULL,
	serial_number int8 NOT NULL,
	filing_date varchar(20) NULL DEFAULT NULL::character varying,
	status_code varchar(30) NULL DEFAULT NULL::character varying,
	status_date varchar(20) NULL DEFAULT NULL::character varying,
	mark_identification varchar(1024) NULL DEFAULT NULL::character varying,
	mark_drawing_code varchar(20) NULL DEFAULT NULL::character varying,
	attorney_docket_number varchar(50) NULL DEFAULT NULL::character varying,
	attorney_name varchar(4096) NULL DEFAULT NULL::character varying,
	principal_register_amended_in varchar(70) NULL DEFAULT NULL::character varying,
	supplemental_register_amended_in varchar(3) NULL DEFAULT NULL::character varying,
	trademark_in varchar(3) NULL DEFAULT NULL::character varying,
	collective_trademark_in varchar(3) NULL DEFAULT NULL::character varying,
	service_mark_in varchar(3) NULL DEFAULT NULL::character varying,
	collective_service_mark_in varchar(3) NULL DEFAULT NULL::character varying,
	collective_membership_mark_in varchar(3) NULL DEFAULT NULL::character varying,
	certification_mark_in varchar(3) NULL DEFAULT NULL::character varying,
	cancellation_pending_in varchar(3) NULL DEFAULT NULL::character varying,
	published_concurrent_in varchar(3) NULL DEFAULT NULL::character varying,
	concurrent_use_in varchar(3) NULL DEFAULT NULL::character varying,
	concurrent_use_proceeding_in varchar(3) NULL,
	interference_pending_in varchar(3) NULL DEFAULT NULL::character varying,
	opposition_pending_in varchar(3) NULL DEFAULT NULL::character varying,
	section_12c_in varchar(3) NULL DEFAULT NULL::character varying,
	section_2f_in varchar(3) NULL DEFAULT NULL::character varying,
	section_2f_in_part_in varchar(3) NULL DEFAULT NULL::character varying,
	renewal_filed_in varchar(3) NULL,
	section_8_filed_in varchar(3) NULL DEFAULT NULL::character varying,
	section_8_partial_accept_in varchar(3) NULL DEFAULT NULL::character varying,
	section_8_accepted_in varchar(3) NULL DEFAULT NULL::character varying,
	section_15_acknowledged_in varchar(3) NULL DEFAULT NULL::character varying,
	section_15_filed_in varchar(3) NULL DEFAULT NULL::character varying,
	supplemental_register_in varchar(3) NULL DEFAULT NULL::character varying,
	foreign_priority_in varchar(3) NULL DEFAULT NULL::character varying,
	change_registration_in varchar(3) NULL,
	intent_to_use_in varchar(3) NULL,
	intent_to_use_current_in varchar(3) NULL DEFAULT NULL::character varying,
	filed_as_use_application_in varchar(3) NULL DEFAULT NULL::character varying,
	amended_to_use_application_in varchar(3) NULL DEFAULT NULL::character varying,
	use_application_currently_in varchar(3) NULL DEFAULT NULL::character varying,
	amended_to_itu_application_in varchar(3) NULL DEFAULT NULL::character varying,
	filing_basis_filed_as_44d_in varchar(3) NULL DEFAULT NULL::character varying,
	amended_to_44d_application_in varchar(3) NULL DEFAULT NULL::character varying,
	filing_basis_current_44d_in varchar(3) NULL DEFAULT NULL::character varying,
	filing_basis_filed_as_44e_in varchar(3) NULL DEFAULT NULL::character varying,
	filing_basis_current_44e_in varchar(3) NULL DEFAULT NULL::character varying,
	amended_to_44e_application_in varchar(3) NULL DEFAULT NULL::character varying,
	without_basis_currently_in varchar(3) NULL DEFAULT NULL::character varying,
	filing_current_no_basis_in varchar(3) NULL DEFAULT NULL::character varying,
	color_drawing_filed_in varchar(3) NULL DEFAULT NULL::character varying,
	color_drawing_current_in varchar(3) NULL DEFAULT NULL::character varying,
	drawing_3d_filed_in varchar(3) NULL DEFAULT NULL::character varying,
	drawing_3d_current_in varchar(3) NULL DEFAULT NULL::character varying,
	standard_characters_claimed_in varchar(3) NULL DEFAULT NULL::character varying,
	filing_basis_filed_as_66a_in varchar(3) NULL DEFAULT NULL::character varying,
	filing_basis_current_66a_in varchar(3) NULL DEFAULT NULL::character varying,
	current_location varchar(70) NULL DEFAULT NULL::character varying,
	location_date varchar(20) NULL DEFAULT NULL::character varying,
	employee_name varchar(70) NULL DEFAULT NULL::character varying,
	registration_date varchar(20) NULL DEFAULT NULL::character varying,
	published_for_opposition_date varchar(20) NULL DEFAULT NULL::character varying,
	amend_to_register_date varchar(20) NULL DEFAULT NULL::character varying,
	abandonment_date varchar(20) NULL DEFAULT NULL::character varying,
	cancellation_code varchar(20) NULL DEFAULT NULL::character varying,
	cancellation_date varchar(20) NULL DEFAULT NULL::character varying,
	republished_12c_date varchar(20) NULL DEFAULT NULL::character varying,
	domestic_representative_name varchar(1024) NULL DEFAULT NULL::character varying,
	renewal_date varchar(20) NULL DEFAULT NULL::character varying,
	law_office_assigned_location_code text NULL,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	CONSTRAINT trademark_app_case_file_headers_pkey PRIMARY KEY (id),
	CONSTRAINT trademark_app_case_file_headers_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_case_file_headers USING btree (serial_number);


-- trademark_app_case_file_owners definition

CREATE TABLE trademark_app_case_file_owners (
	serial_number int8 NOT NULL,
	entry_number varchar(30) NULL DEFAULT NULL::character varying,
	party_type varchar(30) NULL DEFAULT NULL::character varying,
	nationality varchar(50) NULL DEFAULT NULL::character varying,
	legal_entity_type_code varchar(30) NULL DEFAULT NULL::character varying,
	entity_statement varchar(1024) NULL DEFAULT NULL::character varying,
	party_name text NULL,
	address_1 varchar(1024) NULL DEFAULT NULL::character varying,
	address_2 varchar(1024) NULL DEFAULT NULL::character varying,
	city varchar(50) NULL DEFAULT NULL::character varying,
	state varchar(50) NULL DEFAULT NULL::character varying,
	country varchar(5) NULL DEFAULT NULL::character varying,
	other varchar(30) NULL DEFAULT NULL::character varying,
	postcode varchar(20) NULL DEFAULT NULL::character varying,
	dba_aka_text varchar(1024) NULL DEFAULT NULL::character varying,
	composed_of_statement text NULL DEFAULT NULL::character varying,
	name_change_explanation varchar(1024) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	id bigserial NOT NULL,
	CONSTRAINT trademark_app_case_file_owners_pkey PRIMARY KEY (id),
	CONSTRAINT trademark_app_case_file_owners_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_case_file_owners USING btree (serial_number);


-- trademark_app_case_file_statements definition

CREATE TABLE trademark_app_case_file_statements (
	id bigserial NOT NULL,
	serial_number int8 NOT NULL,
	"text" text NULL,
	type_code varchar(30) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	CONSTRAINT trademark_app_case_file_statements_pkey PRIMARY KEY (id),
	CONSTRAINT trademark_app_case_file_statements_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_case_file_statements USING btree (serial_number);


-- trademark_app_classifications definition

CREATE TABLE trademark_app_classifications (
	serial_number int8 NOT NULL,
	international_code_total_no varchar(20) NULL DEFAULT NULL::character varying,
	us_code_total_no varchar(20) NULL DEFAULT NULL::character varying,
	international_code varchar(1024) NULL DEFAULT NULL::character varying,
	status_code varchar(30) NULL DEFAULT NULL::character varying,
	status_date varchar(20) NULL DEFAULT NULL::character varying,
	first_use_anywhere_date varchar(20) NULL DEFAULT NULL::character varying,
	first_use_in_commerce_date varchar(20) NULL DEFAULT NULL::character varying,
	primary_code varchar(30) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	id bigserial NOT NULL,
	CONSTRAINT trademark_app_classifications_pkey PRIMARY KEY (id),
	CONSTRAINT trademark_app_classifications_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_classifications USING btree (serial_number);


-- trademark_app_correspondents definition

CREATE TABLE trademark_app_correspondents (
	serial_number int8 NOT NULL,
	address_1 varchar(50) NULL DEFAULT NULL::character varying,
	address_2 varchar(50) NULL DEFAULT NULL::character varying,
	address_3 varchar(50) NULL DEFAULT NULL::character varying,
	address_4 varchar(50) NULL DEFAULT NULL::character varying,
	address_5 varchar(50) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	id bigserial NOT NULL,
	CONSTRAINT trademark_app_correspondents_pkey PRIMARY KEY (id),
	CONSTRAINT trademark_app_correspondents_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_correspondents USING btree (serial_number);


-- trademark_app_design_searches definition

CREATE TABLE trademark_app_design_searches (
	serial_number int8 NOT NULL,
	code varchar(30) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	id bigserial NOT NULL,
	CONSTRAINT trademark_app_design_searches_pkey PRIMARY KEY (id),
	CONSTRAINT trademark_app_design_searches_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_design_searches USING btree (serial_number);


-- trademark_app_foreign_applications definition

CREATE TABLE trademark_app_foreign_applications (
	serial_number int8 NOT NULL,
	filing_date varchar(20) NULL DEFAULT NULL::character varying,
	registration_date varchar(20) NULL DEFAULT NULL::character varying,
	registration_expiration_date varchar(20) NULL DEFAULT NULL::character varying,
	registration_renewal_date varchar(20) NULL DEFAULT NULL::character varying,
	registration_renewal_expiration_date varchar(20) NULL DEFAULT NULL::character varying,
	entry_number varchar(20) NULL DEFAULT NULL::character varying,
	application_number varchar(20) NULL DEFAULT NULL::character varying,
	country varchar(5) NULL DEFAULT NULL::character varying,
	other varchar(30) NULL DEFAULT NULL::character varying,
	registration_number varchar(20) NULL DEFAULT NULL::character varying,
	renewal_number varchar(20) NULL DEFAULT NULL::character varying,
	foreign_priority_claim_in varchar(3) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	id bigserial NOT NULL,
	CONSTRAINT trademark_app_foreign_applications_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_foreign_applications USING btree (serial_number);


-- trademark_app_international_registration definition

CREATE TABLE trademark_app_international_registration (
	serial_number int8 NOT NULL,
	international_registration_number varchar(30) NULL DEFAULT NULL::character varying,
	international_registration_date varchar(20) NULL DEFAULT NULL::character varying,
	international_publication_date varchar(20) NULL DEFAULT NULL::character varying,
	international_renewal_date varchar(20) NULL DEFAULT NULL::character varying,
	auto_protection_date varchar(20) NULL DEFAULT NULL::character varying,
	international_death_date varchar(20) NULL DEFAULT NULL::character varying,
	international_status_code varchar(30) NULL DEFAULT NULL::character varying,
	international_status_date varchar(20) NULL DEFAULT NULL::character varying,
	priority_claimed_in varchar(30) NULL DEFAULT NULL::character varying,
	priority_claimed_date varchar(20) NULL DEFAULT NULL::character varying,
	first_refusal_in varchar(30) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	id bigserial NOT NULL,
	CONSTRAINT trademark_app_international_registration_pkey PRIMARY KEY (id),
	CONSTRAINT trademark_app_international_registration_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_international_registration USING btree (serial_number);


-- trademark_app_madrid_history_events definition

CREATE TABLE trademark_app_madrid_history_events (
	serial_number int8 NOT NULL,
	code varchar(30) NULL DEFAULT NULL::character varying,
	"date" varchar(20) NULL DEFAULT NULL::character varying,
	description_text varchar(70) NULL DEFAULT NULL::character varying,
	entry_number varchar(30) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	id bigserial NOT NULL,
	madrid_international_filing_record_id int8 NOT NULL,
	CONSTRAINT trademark_app_madrid_history_events_pkey PRIMARY KEY (id),
	CONSTRAINT trademark_app_madrid_history_events_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_madrid_history_events USING btree (serial_number);
CREATE INDEX ON trademark_app_madrid_history_events USING btree (madrid_international_filing_record_id);


-- trademark_app_madrid_international_filing_record definition

CREATE TABLE trademark_app_madrid_international_filing_record (
	serial_number int8 NOT NULL,
	entry_number varchar(20) NULL DEFAULT NULL::character varying,
	reference_number varchar(30) NULL DEFAULT NULL::character varying,
	original_filing_date_uspto varchar(20) NULL DEFAULT NULL::character varying,
	international_registration_number varchar(30) NULL DEFAULT NULL::character varying,
	international_registration_date varchar(20) NULL DEFAULT NULL::character varying,
	international_status_code text NULL,
	international_status_date varchar(20) NULL DEFAULT NULL::character varying,
	irregularity_reply_by_date varchar(20) NULL DEFAULT NULL::character varying,
	international_renewal_date varchar(20) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	id bigserial NOT NULL,
	CONSTRAINT trademark_app_madrid_international_filing_record_pkey PRIMARY KEY (id),
	CONSTRAINT trademark_app_madrid_international_filing_re_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_madrid_international_filing_record USING btree (serial_number);


-- trademark_app_prior_registration_applications definition

CREATE TABLE trademark_app_prior_registration_applications (
	id bigserial NOT NULL,
	serial_number int8 NOT NULL,
	other_related_in varchar(3) NULL DEFAULT NULL::character varying,
	relationship_type varchar(3) NULL DEFAULT NULL::character varying,
	"number" varchar(20) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	CONSTRAINT trademark_app_prior_registration_applications1_pkey PRIMARY KEY (id),
	CONSTRAINT trademark_app_prior_registration_application_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_prior_registration_applications USING btree (serial_number);


-- trademark_app_us_codes definition

CREATE TABLE trademark_app_us_codes (
	serial_number int8 NOT NULL,
	classification_id int8 NOT NULL,
	us_code varchar(30) NULL DEFAULT NULL::character varying,
	created timestamptz NOT NULL DEFAULT now(),
	modified timestamptz NOT NULL DEFAULT now(),
	status bool NOT NULL DEFAULT true,
	id bigserial NOT NULL,
	CONSTRAINT trademark_app_us_codes_pkey PRIMARY KEY (id),
	CONSTRAINT trademark_app_us_codes_serial_number_fkey FOREIGN KEY (serial_number) REFERENCES trademark_app_case_files(serial_number) ON DELETE CASCADE
);
CREATE INDEX ON trademark_app_us_codes USING btree (serial_number);
