from sysdata.config.production_config import get_production_config
from syscore.fileutils import resolve_path_and_filename_for_package
from sysdata.csv.csv_futures_contract_prices import ConfigCsvFuturesPrices
from syscore.dateutils import HOURLY_FREQ, DAILY_PRICE_FREQ
from sysinit.futures.contract_prices_from_csv_to_arctic import (
	# init_db_with_csv_futures_contract_prices,
	init_db_with_csv_futures_contract_prices_for_code
)
from sysinit.futures.instrument_barchart_sets import instrument_barchart_set, instrument_barchart_set_no_hourly

if __name__ == "__main__":
	BARCHART_CONFIG = ConfigCsvFuturesPrices(
		input_date_index_name="Time",
		input_skiprows=0,
		input_skipfooter=0,
		input_date_format="%Y-%m-%dT%H:%M:%S%z",
		input_column_mapping=dict(
			OPEN="Open", HIGH="High", LOW="Low", FINAL="Close", VOLUME="Volume"
		)
	)

	# assuming bc-utils config pasted into private
	data_path = resolve_path_and_filename_for_package(get_production_config().get_element_or_default("barchart_path", None))
	print("Insert instrument code:\n")
	instrument_code: str = input()
	if instrument_code not in instrument_barchart_set:
		raise ValueError

	if instrument_code not in instrument_barchart_set_no_hourly:
		init_db_with_csv_futures_contract_prices_for_code(
			instrument_code,
			data_path,
			csv_config=BARCHART_CONFIG,
			frequency=DAILY_PRICE_FREQ
		)
		init_db_with_csv_futures_contract_prices_for_code(
			instrument_code,
			data_path,
			csv_config=BARCHART_CONFIG,
			frequency=HOURLY_FREQ
		)
	else:
		init_db_with_csv_futures_contract_prices_for_code(
			instrument_code,
			data_path,
			csv_config=BARCHART_CONFIG,
			frequency=DAILY_PRICE_FREQ,
			force_copy_to_mixed=True
		)
