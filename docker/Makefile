.ONESHELL:

init:
	echo CORE_DEBUG=false >> .env
	echo CORE_DATABASE_URL=psql://postgres:postgres@postgres:5432/core_db >> .env
	echo CORE_ALLOWED_HOSTS=127.0.0.1 >> .env
	echo SECRET_KEY="s4ea6pdiqh5w9w&cxkhb0_05+tr+s!2n$+7x%_qb%faw+1$q@" >> .env
	echo CHC_BLACK_API_KEY=it3r63j1c4d32ef44q8laki7ej44or4f >> .env
	echo CHC_BLACK_SECRET_KEY=jbgve73i5e8ajhcnqtvmpgk96qj2c91j4h663pffv5ovosv13abha1hu5bibjgpa >> .env
    echo MERCHANT_ID=231915 >> .env
    echo FIRST_SECRET=muibr9gf >> .env
    echo SECOND_SECRET=uf44bxhn >> .env
    echo TG_API_ID=567238 >> .env
    echo TG_API_HASH=a7e1581760e680629ab397765857e862 >> .env
    echo TG_API_TOKEN=1422793511:AAF-fDtEgxqFP5V68ADgjd7h7tAXRWQ5IZE >> .env
    echo BOT_USERNAME=megawingamesbot >> .env
	cp .env ../api/core/config/settings
    cp .env ../bot/config/settings



build:
	docker-compose -f local.yml build

up:
	docker-compose -f local.yml up
