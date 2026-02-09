# 🤝 Guia de Contribuição

Obrigado por considerar contribuir para este projeto!

## Como Contribuir

### 1. Fork e Clone

```bash
git clone https://github.com/seu-usuario/data-pipeline-monitoring.git
cd data-pipeline-monitoring
```

### 2. Crie uma Branch

```bash
git checkout -b feature/minha-contribuicao
```

### 3. Configure o Ambiente

```bash
make init
```

### 4. Faça suas Alterações

#### Adicionando um DAG

1. Crie o arquivo em `airflow/dags/`
2. Adicione testes em `tests/dags/`
3. Documente o DAG com docstrings
4. Adicione tags apropriadas

#### Criando um Dashboard

1. Crie no Grafana UI
2. Exporte como JSON
3. Salve em `monitoring/grafana/dashboards/`
4. Documente no README

#### Adicionando Alertas

1. Edite `monitoring/prometheus/alerts.yml`
2. Teste com `promtool check rules`
3. Documente o alerta

### 5. Teste suas Alterações

```bash
# Validar DAGs
make test-dags

# Verificar formatação
make format-dags
make lint-dags

# Testar build
make build

# Verificar saúde
make check-health
```

### 6. Commit e Push

Use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git add .
git commit -m "feat: adiciona novo dashboard de performance"
git push origin feature/minha-contribuicao
```

Padrões de commit:
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

### 7. Abra um Pull Request

1. Vá para o repositório no GitHub
2. Clique em "New Pull Request"
3. Descreva suas mudanças
4. Aguarde revisão

## Diretrizes

### Código Python

- Siga PEP 8
- Use type hints
- Docstrings em todas as funções
- Máximo 100 caracteres por linha

### DAGs

- Sempre adicione `default_args`
- Use tags descritivas
- Documente o propósito do DAG
- Implemente retry logic
- Configure SLAs quando apropriado

### Dashboards

- Use nomes descritivos
- Agrupe métricas relacionadas
- Adicione descrições nos painéis
- Configure alertas visuais

### Documentação

- Atualize README.md se necessário
- Adicione exemplos de uso
- Documente configurações
- Mantenha QUICKSTART.md atualizado

## Reportando Bugs

Use o template de issue:

```markdown
**Descrição**
Descrição clara do bug

**Como Reproduzir**
1. Vá para '...'
2. Clique em '....'
3. Veja o erro

**Comportamento Esperado**
O que deveria acontecer

**Screenshots**
Se aplicável

**Ambiente**
- OS: [e.g. Ubuntu 22.04]
- Docker: [e.g. 20.10.21]
- Browser: [e.g. Chrome 120]
```

## Sugerindo Melhorias

- Descreva a melhoria claramente
- Explique o benefício
- Forneça exemplos se possível

## Código de Conduta

- Seja respeitoso e inclusivo
- Aceite feedback construtivo
- Foque no que é melhor para o projeto
- Ajude outros contribuidores

## Dúvidas?

- Abra uma issue de discussão
- Entre em contato com os mantenedores

Obrigado por contribuir! 🚀
