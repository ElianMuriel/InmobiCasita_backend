-- Script para limpiar la base de datos y empezar de cero
-- ⚠️ ADVERTENCIA: Esto eliminará todos los datos excepto el usuario admin

-- 1. Ver qué hay antes de limpiar
SELECT 'ANTES DE LIMPIAR:' as info;
SELECT 'Clientes' as tabla, COUNT(*) as total FROM gestion_cliente
UNION ALL
SELECT 'Propietarios', COUNT(*) FROM gestion_propietario
UNION ALL
SELECT 'Inmuebles', COUNT(*) FROM gestion_inmueble
UNION ALL
SELECT 'Visitas', COUNT(*) FROM gestion_visita
UNION ALL
SELECT 'Contratos', COUNT(*) FROM gestion_contrato
UNION ALL
SELECT 'Pagos', COUNT(*) FROM gestion_pago
UNION ALL
SELECT 'Usuarios', COUNT(*) FROM auth_user;

-- 2. Eliminar datos relacionados primero (por foreign keys)
DELETE FROM gestion_pago;
DELETE FROM gestion_contrato;
DELETE FROM gestion_visita;
DELETE FROM gestion_inmueble;

-- 3. Eliminar clientes y propietarios
DELETE FROM gestion_cliente;
DELETE FROM gestion_propietario;

-- 4. Mantener el usuario admin (no eliminamos auth_user)
-- Si quieres eliminar otros usuarios que no sean admin, descomenta:
-- DELETE FROM auth_user WHERE is_superuser = false AND id != 1;

-- 5. Mantener tipos de inmueble y roles (son datos de referencia)
-- Si quieres limpiarlos también, descomenta:
-- DELETE FROM gestion_tipoinmueble;
-- DELETE FROM gestion_rol;

-- 6. Reiniciar secuencias (para que los IDs empiecen desde 1)
ALTER SEQUENCE gestion_cliente_id_seq RESTART WITH 1;
ALTER SEQUENCE gestion_propietario_id_seq RESTART WITH 1;
ALTER SEQUENCE gestion_inmueble_id_seq RESTART WITH 1;
ALTER SEQUENCE gestion_visita_id_seq RESTART WITH 1;
ALTER SEQUENCE gestion_contrato_id_seq RESTART WITH 1;
ALTER SEQUENCE gestion_pago_id_seq RESTART WITH 1;

-- 7. Verificar que quedó limpio
SELECT 'DESPUÉS DE LIMPIAR:' as info;
SELECT 'Clientes' as tabla, COUNT(*) as total FROM gestion_cliente
UNION ALL
SELECT 'Propietarios', COUNT(*) FROM gestion_propietario
UNION ALL
SELECT 'Inmuebles', COUNT(*) FROM gestion_inmueble
UNION ALL
SELECT 'Visitas', COUNT(*) FROM gestion_visita
UNION ALL
SELECT 'Contratos', COUNT(*) FROM gestion_contrato
UNION ALL
SELECT 'Pagos', COUNT(*) FROM gestion_pago
UNION ALL
SELECT 'Usuarios', COUNT(*) FROM auth_user;
