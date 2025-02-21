SELECT
    segmento,
    id_modulo,
    modulo
FROM ep_dw.modulo
WHERE
    (:modulos IS NULL OR id_modulo = ANY(:modulos))
