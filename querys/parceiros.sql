SELECT 
    part,
    CASE WHEN pais = 'Brasil' THEN estado ELSE pais END AS regiao,
    COALESCE(grupo_empresarial, grupo_representacao) AS grupo
FROM ep_dw.parceiro
