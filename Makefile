# Makefile to gather common commands

.PHONY: clean format help lint pipenv-dev-install
.DEFAULT_GOAL := help

# Project variables
SRC:=src/$(MODULE)

help: ## Show this help menu
	$(info Available make commands:)
	@grep -e '^[a-z|_|-]*:.* ##' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS=":.* ## "}; {printf "\t%-23s %s\n", $$1, $$2};'

.print-phony:
	@echo "\n.PHONY: "
	@grep '^[a-z|_|-]*:.* ##' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS=":.* ## "}; {printf "%s ", $$1};'
	@echo "\n"

####### COMMANDS #######################################################################

clean: ## Clean up auxiliary and temporary files from the workspace
	$(info Cleaning auxiliary and temporary files...)
	@find . -maxdepth 1 -type d -name '.mypy_cache' -exec rm -r {} +
	@find . -maxdepth 1 -type d -name '.ruff_cache' -exec rm -r {} +
	@find . -maxdepth 1 -type d -name 'build'       -exec rm -r {} +
	@find . -maxdepth 1 -type d -name 'dist'        -exec rm -r {} +
	@find . -maxdepth 2 -type d -name '*.egg-info'  -exec rm -r {} +
	@echo Done.

format: ## Format the entire codebase
	@if \
	type black >/dev/null 2>&1 ; then \
		echo Formatting source-code... && \
		echo Applying black... && \
		black -q $(SRC) && \
		echo Done. ; \
	else echo SKIPPED. Run 'make pipenv-dev-install' first. >&2 ; fi

lint: ## Perform a static code analysis
	@if \
	type ruff >/dev/null 2>&1 ; then \
		echo Linting source-code... && \
		echo Applying ruff... && \
		ruff check $(SRC) && \
		echo Done. ; \
	else echo SKIPPED. Run 'make pipenv-dev-install' first. >&2 ; fi

pipenv-dev-install: ## Create dev venv
	@pipenv run pip install --upgrade pip
	@pipenv install --dev --ignore-pipfile --deploy

docker-build: ## Build all Dockerfile images for onebrc
	@docker build -f dockerfiles/cpython.Dockerfile -t onebrc-cpython .
	@docker build -f dockerfiles/cpython_perf.Dockerfile -t onebrc-cpython_perf .

docker-build-modin: ## Build all Dockerfile images for onebrc
	@docker build -f dockerfiles/cpython.modin.Dockerfile -t onebrc-cpython-modin .
	@docker build -f dockerfiles/cpython_perf.modin.Dockerfile -t onebrc-cpython_perf-modin .

run-cpython-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@python -m onebrc.00_native_DictReader /onebrc/test_data/100t.txt --avg 10 -t 120
	@python -m onebrc.01_native_split /onebrc/test_data/100t.txt --avg 10 -t 120
	@python -m onebrc.02_native_read_text /onebrc/test_data/100t.txt --avg 10 -t 120

run-cpython-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@python -m onebrc.00_native_DictReader /onebrc/test_data/100m.txt --avg 10 -t 120
	@python -m onebrc.01_native_split /onebrc/test_data/100m.txt --avg 10 -t 120
	@python -m onebrc.02_native_read_text /onebrc/test_data/100m.txt --avg 10 -t 120

run-cpython-no-gc-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@python -m onebrc.00_native_DictReader_no_gc /onebrc/test_data/100t.txt --avg 10 -t 120
	@python -m onebrc.01_native_split_no_gc /onebrc/test_data/100t.txt --avg 10 -t 120
	@python -m onebrc.02_native_read_text_no_gc /onebrc/test_data/100t.txt --avg 10 -t 120

run-cpython-no-gc-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@python -m onebrc.00_native_DictReader_no_gc /onebrc/test_data/100m.txt --avg 10 -t 120
	@python -m onebrc.01_native_split_no_gc /onebrc/test_data/100m.txt --avg 10 -t 120
	@python -m onebrc.02_native_read_text_no_gc /onebrc/test_data/100m.txt --avg 10 -t 120

run-pandas-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@python -m onebrc.03_pandas /onebrc/test_data/100t.txt --avg 10 -t 120
	@python -m onebrc.03_pandas_pyarrow /onebrc/test_data/100t.txt --avg 10 -t 120

run-pandas-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@python -m onebrc.03_pandas /onebrc/test_data/100m.txt --avg 10 -t 120
	@python -m onebrc.03_pandas_pyarrow /onebrc/test_data/100m.txt --avg 10 -t 120

run-dask-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@python -m onebrc.04_dask /onebrc/test_data/100t.txt --avg 10 -t 120
	@python -m onebrc.04_dask_pyarrow /onebrc/test_data/100t.txt --avg 10 -t 120

run-dask-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@python -m onebrc.04_dask /onebrc/test_data/100m.txt --avg 10 -t 120
	@python -m onebrc.04_dask_pyarrow /onebrc/test_data/100m.txt --avg 10 -t 120

run-modin-ray-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@MODIN_ENGINE=ray python -m onebrc.05_modin_ray /onebrc/test_data/100t.txt --avg 10 -t 120

run-modin-ray-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@MODIN_ENGINE=ray python -m onebrc.05_modin_ray /onebrc/test_data/100m.txt --avg 10 -t 120

run-polars-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@python -m onebrc.06_polars_read_csv /onebrc/test_data/100t.txt --avg 10 -t 120
	@python -m onebrc.06_polars_scan_csv /onebrc/test_data/100t.txt --avg 10 -t 120
	@python -m onebrc.06_polars_scan_csv_streaming /onebrc/test_data/100t.txt --avg 10 -t 120

run-polars-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@python -m onebrc.06_polars_read_csv /onebrc/test_data/100m.txt --avg 10 -t 120
	@python -m onebrc.06_polars_scan_csv /onebrc/test_data/100m.txt --avg 10 -t 120
	@python -m onebrc.06_polars_scan_csv_streaming /onebrc/test_data/100m.txt --avg 10 -t 120

run-polars-200m-docker: ## Run all modules inside a docker container using 200m.txt
	@python -m onebrc.06_polars_read_csv /onebrc/test_data/200m.txt --avg 10 -t 120; \
		python -m onebrc.06_polars_scan_csv /onebrc/test_data/200m.txt --avg 10 -t 120; \
		python -m onebrc.06_polars_scan_csv_streaming /onebrc/test_data/200m.txt --avg 10 -t 120

run-polars-1b-docker: ## Run all modules inside a docker container using 1b.txt
	@python -m onebrc.06_polars_read_csv /onebrc/test_data/1b.txt --avg 10 -t 120; \
		python -m onebrc.06_polars_scan_csv /onebrc/test_data/1b.txt --avg 10 -t 120; \
		python -m onebrc.06_polars_scan_csv_streaming /onebrc/test_data/1b.txt --avg 10 -t 120

run-duckdb-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@python -m onebrc.07_duckdb /onebrc/test_data/100t.txt --avg 10 -t 120
	@python -m onebrc.07_duckdb_parallel /onebrc/test_data/100t.txt --avg 10 -t 120

run-duckdb-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@python -m onebrc.07_duckdb /onebrc/test_data/100m.txt --avg 10 -t 120
	@python -m onebrc.07_duckdb_parallel /onebrc/test_data/100m.txt --avg 10 -t 120

run-duckdb-200m-docker: ## Run all modules inside a docker container using 200m.txt
	@python -m onebrc.07_duckdb /onebrc/test_data/200m.txt --avg 10 -t 120; \
		python -m onebrc.07_duckdb_parallel /onebrc/test_data/200m.txt --avg 10 -t 120

run-duckdb-1b-docker: ## Run all modules inside a docker container using 1b.txt
	@python -m onebrc.07_duckdb /onebrc/test_data/1b.txt --avg 10 -t 120; \
		python -m onebrc.07_duckdb_parallel /onebrc/test_data/1b.txt --avg 10 -t 120

run-numpy-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@python -m onebrc.08_numpy /onebrc/test_data/100t.txt --avg 10 -t 120

run-numpy-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@python -m onebrc.08_numpy /onebrc/test_data/100m.txt --avg 10 -t 120

run-pyarrow-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@python -m onebrc.09_pyarrow /onebrc/test_data/100t.txt --avg 10 -t 120

run-pyarrow-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@python -m onebrc.09_pyarrow /onebrc/test_data/100m.txt --avg 10 -t 120

run-pyarrow-200m-docker: ## Run all modules inside a docker container using 200m.txt;
	@python -m onebrc.09_pyarrow /onebrc/test_data/200m.txt --avg 10 -t 120

run-pyarrow-1b-docker: ## Run all modules inside a docker container using 1b.txt;
	@python -m onebrc.09_pyarrow /onebrc/test_data/1b.txt --avg 10 -t 120

run-parquet-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@echo Compression: uncompressed; \
		python -m onebrc.10_parquet_polars_read_parquet /onebrc/test_data/100t.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet /onebrc/test_data/100t.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet_streaming /onebrc/test_data/100t.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_duckdb /onebrc/test_data/100t.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow /onebrc/test_data/100t.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow_memory_map /onebrc/test_data/100t.txt.uncompressed.parquet --avg 10 -t 120
	@echo Compression: lz4; \
		python -m onebrc.10_parquet_polars_read_parquet /onebrc/test_data/100t.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet /onebrc/test_data/100t.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet_streaming /onebrc/test_data/100t.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_duckdb /onebrc/test_data/100t.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow /onebrc/test_data/100t.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow_memory_map /onebrc/test_data/100t.txt.lz4.parquet --avg 10 -t 120

run-parquet-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@echo Compression: uncompressed; \
		python -m onebrc.10_parquet_polars_read_parquet /onebrc/test_data/100m.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet /onebrc/test_data/100m.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet_streaming /onebrc/test_data/100m.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_duckdb /onebrc/test_data/100m.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow /onebrc/test_data/100m.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow_memory_map /onebrc/test_data/100m.txt.uncompressed.parquet --avg 10 -t 120
	@echo Compression: lz4; \
		python -m onebrc.10_parquet_polars_read_parquet /onebrc/test_data/100m.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet /onebrc/test_data/100m.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet_streaming /onebrc/test_data/100m.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_duckdb /onebrc/test_data/100m.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow /onebrc/test_data/100m.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow_memory_map /onebrc/test_data/100m.txt.lz4.parquet --avg 10 -t 120

run-parquet-200m-docker: ## Run all modules inside a docker container using 200m.txt;
	@echo Compression: uncompressed; \
		python -m onebrc.10_parquet_polars_read_parquet /onebrc/test_data/200m.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet /onebrc/test_data/200m.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet_streaming /onebrc/test_data/200m.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_duckdb /onebrc/test_data/200m.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow /onebrc/test_data/200m.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow_memory_map /onebrc/test_data/200m.txt.uncompressed.parquet --avg 10 -t 120
	@echo Compression: lz4; \
		python -m onebrc.10_parquet_polars_read_parquet /onebrc/test_data/200m.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet /onebrc/test_data/200m.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet_streaming /onebrc/test_data/200m.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_duckdb /onebrc/test_data/200m.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow /onebrc/test_data/200m.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow_memory_map /onebrc/test_data/200m.txt.lz4.parquet --avg 10 -t 120

run-parquet-1b-docker: ## Run all modules inside a docker container using 1b.txt;
	@echo Compression: uncompressed; \
		python -m onebrc.10_parquet_polars_read_parquet /onebrc/test_data/1b.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet /onebrc/test_data/1b.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet_streaming /onebrc/test_data/1b.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_duckdb /onebrc/test_data/1b.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow /onebrc/test_data/1b.txt.uncompressed.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow_memory_map /onebrc/test_data/1b.txt.uncompressed.parquet --avg 10 -t 120; \
	echo Compression: lz4; \
		python -m onebrc.10_parquet_polars_read_parquet /onebrc/test_data/1b.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet /onebrc/test_data/1b.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_polars_scan_parquet_streaming /onebrc/test_data/1b.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_duckdb /onebrc/test_data/1b.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow /onebrc/test_data/1b.txt.lz4.parquet --avg 10 -t 120; \
		python -m onebrc.10_parquet_pyarrow_memory_map /onebrc/test_data/1b.txt.lz4.parquet --avg 10 -t 120

run-duckdb_db-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@python -m onebrc.11_duckdb_duckdb /onebrc/test_data/100t.txt.duckdb --avg 10 -t 120

run-duckdb_db-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@python -m onebrc.11_duckdb_duckdb /onebrc/test_data/100m.txt.duckdb --avg 10 -t 120

run-duckdb_db-200m-docker: ## Run all modules inside a docker container using 200m.txt
	@python -m onebrc.11_duckdb_duckdb /onebrc/test_data/200m.txt.duckdb --avg 10 -t 120

run-duckdb_db-1b-docker: ## Run all modules inside a docker container using 1b.txt
	@python -m onebrc.11_duckdb_duckdb /onebrc/test_data/1b.txt.duckdb --avg 10 -t 120

run-mult_avro_duckdb-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@echo Compression: uncompressed; \
		python -m onebrc.12_mult_avro_duckdb '/onebrc/test_data/100t/avro/*.uncompressed.avro' --avg 10 -t 120;

run-mult_avro_duckdb-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@echo Compression: uncompressed; \
		python -m onebrc.12_mult_avro_duckdb '/onebrc/test_data/100m/avro/*.uncompressed.avro' --avg 10 -t 120

run-mult_avro_duckdb-200m-docker: ## Run all modules inside a docker container using 200m.txt
	@echo Compression: uncompressed; \
		python -m onebrc.12_mult_avro_duckdb '/onebrc/test_data/200m/avro/*.uncompressed.avro' --avg 10 -t 120

run-mult_avro_duckdb-1b-docker: ## Run all modules inside a docker container using 1b.txt
	@echo Compression: uncompressed; \
		python -m onebrc.12_mult_avro_duckdb '/onebrc/test_data/1b/avro/*.uncompressed.avro' --avg 10 -t 120

run-mult_parquet_duckdb-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@echo Compression: uncompressed; \
		python -m onebrc.12_mult_parquet_duckdb '/onebrc/test_data/100t/parquet/*.uncompressed.parquet' --avg 10 -t 120;

run-mult_parquet_duckdb-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@echo Compression: uncompressed; \
		python -m onebrc.12_mult_parquet_duckdb '/onebrc/test_data/100m/parquet/*.uncompressed.parquet' --avg 10 -t 120

run-mult_parquet_duckdb-200m-docker: ## Run all modules inside a docker container using 200m.txt
	@echo Compression: uncompressed; \
		python -m onebrc.12_mult_parquet_duckdb '/onebrc/test_data/200m/parquet/*.uncompressed.parquet' --avg 10 -t 120

run-mult_parquet_duckdb-1b-docker: ## Run all modules inside a docker container using 1b.txt
	@echo Compression: uncompressed; \
		python -m onebrc.12_mult_parquet_duckdb '/onebrc/test_data/1b/parquet/*.uncompressed.parquet' --avg 10 -t 120

run-avro_duckdb-100t-docker: ## Run all modules inside a docker container using 100t.txt
	@echo Compression: uncompressed; \
		python -m onebrc.13_avro_duckdb '/onebrc/test_data/100t/100t.uncompressed.avro' --avg 10 -t 120;

run-avro_duckdb-100m-docker: ## Run all modules inside a docker container using 100m.txt
	@echo Compression: uncompressed; \
		python -m onebrc.13_avro_duckdb '/onebrc/test_data/100m/100m.uncompressed.avro' --avg 10 -t 120

run-avro_duckdb-200m-docker: ## Run all modules inside a docker container using 200m.txt
	@echo Compression: uncompressed; \
		python -m onebrc.13_avro_duckdb '/onebrc/test_data/200m/200m.uncompressed.avro' --avg 10 -t 120

run-avro_duckdb-1b-docker: ## Run all modules inside a docker container using 1b.txt
	@echo Compression: uncompressed; \
		python -m onebrc.13_avro_duckdb '/onebrc/test_data/1b/1b.uncompressed.avro' --avg 10 -t 120
