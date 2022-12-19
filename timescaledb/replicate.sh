#!/bin/bash

if [[ -z $POSTGRES_REPLICA_SOURCE ]]; then

psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SET password_encryption = 'scram-sha-256'; CREATE ROLE \"$POSTGRES_REPLICA_USER_NAME\" WITH REPLICATION PASSWORD '$POSTGRES_REPLICA_PASSWORD' LOGIN;"

cat >> ${PGDATA}/postgresql.conf <<EOF
listen_addresses= '*'
wal_level = replica
max_wal_senders = 2
max_replication_slots = 2
synchronous_commit = ${POSTGRES_REPLICA_COMMIT_SYNCHRONOUS}
EOF

if [[ "${POSTGRES_REPLICA_COMMIT_SYNCHRONOUS}" =~ ^(on|remote_write|remote_apply)$ ]]; then
cat >> ${PGDATA}/postgresql.conf <<EOF
synchronous_standby_names = '1 (${POSTGRES_REPLICA_NAME})'
EOF
fi

if  [[ -z $POSTGRES_REPLICA_SUBNET ]]; then
    POSTGRES_REPLICA_SUBNET=$(getent hosts ${POSTGRES_REPLICA_DESTINATION} | awk '{ print $1 }')/32
fi

cat >> ${PGDATA}/pg_hba.conf <<EOF
host     replication     ${POSTGRES_REPLICA_USER_NAME}   ${POSTGRES_REPLICA_SUBNET}       trust
host     replication     ${POSTGRES_REPLICA_USER_NAME}   0.0.0.0/8       scram-sha-256
EOF

pg_ctl -D ${PGDATA} -m fast -w restart
psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT * FROM pg_create_physical_replication_slot('${POSTGRES_REPLICA_NAME}_slot');"

else

pg_ctl -D ${PGDATA} -m fast -w stop
rm -rf ${PGDATA}

cat > ~/.pgpass.conf <<EOF
*:${POSTGRESQL_PORTNUMBER}:replication:${POSTGRES_REPLICA_USER_NAME}:${POSTGRES_REPLICA_PASSWORD}
EOF

chown postgres:postgres ~/.pgpass.conf
chmod 0600 ~/.pgpass.conf

until PGPASSFILE=~/.pgpass.conf pg_basebackup -h ${POSTGRES_REPLICA_SOURCE} -D ${PGDATA} -U ${POSTGRES_REPLICA_USER_NAME} -vP -w
do
    sleep 1
    echo "Retrying..."
done

rm ~/.pgpass.conf

echo -n > ${PGDATA}/standby.signal

cat > ${PGDATA}/postgresql.auto.conf <<EOF
primary_conninfo = 'host=${POSTGRES_REPLICA_SOURCE} port=${POSTGRESQL_PORTNUMBER} user=${POSTGRES_REPLICA_USER_NAME} password=${POSTGRES_REPLICA_PASSWORD} application_name=${POSTGRES_REPLICA_NAME}'
primary_slot_name = '${POSTGRES_REPLICA_NAME}_slot'
EOF

pg_ctl -D ${PGDATA} -w start

fi
