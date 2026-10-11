# Instruções para o Claude

Ao implementar ou alterar qualquer código Python (`src/presenca/`, `tests/` ou os scripts em `pesquisa/`), siga os padrões definidos em [docs/arquitetura.md](docs/arquitetura.md):

@docs/arquitetura.md

Antes de concluir uma implementação:

- confira a regra de dependência (casos de uso e domínio nunca importam adaptadores nem bibliotecas externas);
- crie ou atualize o fake da porta em `tests/fakes.py` e os testes correspondentes;
- rode `python -m pytest` e `ruff check .` e reporte o resultado.
