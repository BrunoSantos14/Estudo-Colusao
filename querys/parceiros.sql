SELECT 
    part,
    CASE WHEN pais = 'Brasil' THEN estado ELSE pais AS regiao,
    COALESCE(grupo_empresarial, grupo_representacao) AS grupo
FROM ep_dw.parceiro
WHERE 
    (:parceiros IS NULL OR part = ANY(:parceiros))
