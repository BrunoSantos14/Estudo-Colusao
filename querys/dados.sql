SELECT 
    part,
    id_modulo,
    analito,
    envio envio_str,
    TO_DATE(
        CASE 
            WHEN envio LIKE 'Jan/%' THEN REPLACE(envio, 'Jan', 'Jan')
            WHEN envio LIKE 'Fev/%' THEN REPLACE(envio, 'Fev', 'Feb')
            WHEN envio LIKE 'Mar/%' THEN REPLACE(envio, 'Mar', 'Mar')
            WHEN envio LIKE 'Abr/%' THEN REPLACE(envio, 'Abr', 'Apr')
            WHEN envio LIKE 'Mai/%' THEN REPLACE(envio, 'Mai', 'May')
            WHEN envio LIKE 'Jun/%' THEN REPLACE(envio, 'Jun', 'Jun')
            WHEN envio LIKE 'Jul/%' THEN REPLACE(envio, 'Jul', 'Jul')
            WHEN envio LIKE 'Ago/%' THEN REPLACE(envio, 'Ago', 'Aug')
            WHEN envio LIKE 'Set/%' THEN REPLACE(envio, 'Set', 'Sep')
            WHEN envio LIKE 'Out/%' THEN REPLACE(envio, 'Out', 'Oct')
            WHEN envio LIKE 'Nov/%' THEN REPLACE(envio, 'Nov', 'Nov')
            WHEN envio LIKE 'Dez/%' THEN REPLACE(envio, 'Dez', 'Dec')
        END, 
        'Mon/YYYY') AS envio,
    TRIM(REPLACE(item_ensaio, '\t', '')) item_ensaio,
    sistema,
    valor
FROM ep_dw.fato
WHERE TRUE
    AND ano = :ano
    AND (:id_modulo IS NULL OR id_modulo = ANY(:id_modulo))
    AND (:analito IS NULL OR analito = ANY(:analito))
    AND metodo_calculo = 'Quantitativo Robusto'
    AND ava NOT ILIKE '%nr%'
    AND ava NOT ILIKE '%*%'
    AND envio NOT ILIKE '%esp%'
    AND part <> 8012
    AND item_extra = 0