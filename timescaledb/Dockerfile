ARG TIMESCALEDB_VERSION=2.9.2-pg13

FROM timescale/timescaledb:${TIMESCALEDB_VERSION}

MAINTAINER Anirudh Ramesh

ADD replicate.sh /docker-entrypoint-initdb.d/

