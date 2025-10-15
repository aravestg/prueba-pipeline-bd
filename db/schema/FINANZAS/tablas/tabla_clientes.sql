-- OWNER: FINANZAS | DBSPACE: datadbs_finanzas
-- Estado final
CREATE TABLE FINANZAS:tabla_clientes (
  id_cliente SERIAL PRIMARY KEY,
  rut        CHAR(12) NOT NULL,
  nombre     VARCHAR(120) NOT NULL,
  fecha_alta DATETIME YEAR TO DAY NOT NULL
);
