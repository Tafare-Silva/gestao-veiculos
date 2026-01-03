# 🤝 Contribuindo com o Sistema de Gestão de Veículos

Obrigado por considerar contribuir com este projeto! 

## 📋 Como Contribuir

### 1. Reportar Bugs

Encontrou um bug? Abra uma [issue](https://github.com/Tafarel-silva/gestao-veiculos/issues) incluindo:

- **Descrição clara** do problema
- **Passos para reproduzir** o erro
- **Comportamento esperado** vs **comportamento atual**
- **Screenshots** (se aplicável)
- **Ambiente:** Sistema operacional, versão do Python, navegador

### 2. Sugerir Melhorias

Tem uma ideia? Abra uma issue com a tag `enhancement` incluindo:

- **Descrição da funcionalidade** desejada
- **Por que seria útil** (casos de uso)
- **Como você imagina** que funcionaria

### 3. Fazer Pull Requests

#### Passo a Passo:

```bash
# 1. Fork o projeto no GitHub

# 2. Clone seu fork
git clone https://github.com/Tafarel-silva/gestao-veiculos.git
cd gestao-veiculos

# 3. Crie uma branch para sua feature
git checkout -b feature/minha-feature

# 4. Faça suas alterações

# 5. Commit com mensagens claras
git commit -m "Adiciona funcionalidade X"

# 6. Push para seu fork
git push origin feature/minha-feature

# 7. Abra um Pull Request no GitHub
```

#### Boas Práticas:

- ✅ **Código limpo** e bem comentado
- ✅ **Siga o padrão** PEP 8 (Python)
- ✅ **Teste suas mudanças** antes de enviar
- ✅ **Atualize a documentação** se necessário
- ✅ **Um PR por feature** (não misture várias mudanças)

### 4. Convenções de Commit

Use mensagens de commit claras e descritivas:

```
feat: Adiciona upload de múltiplas imagens
fix: Corrige cálculo de lucro com troca
docs: Atualiza README com novas instruções
style: Melhora responsividade do menu mobile
refactor: Reorganiza views de relatórios
test: Adiciona testes para modelo Veiculo
```

**Prefixos:**
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação, UI/UX
- `refactor:` Refatoração de código
- `test:` Testes
- `chore:` Manutenção, dependências

## 🧪 Testes

Antes de enviar seu PR, certifique-se de:

```bash
# Executar os testes
python manage.py test

# Verificar o código
flake8 .

# Verificar migrations
python manage.py makemigrations --check --dry-run
```

## 📝 Documentação

Ao adicionar novas funcionalidades, atualize:

- README.md (se necessário)
- Docstrings nas funções/classes
- Comentários no código (quando relevante)

## 🎨 Padrões de Código

### Python (Django)

```python
# ✅ BOM
def calcular_lucro_veiculo(veiculo):
    """
    Calcula o lucro de um veículo vendido.
    
    Args:
        veiculo: Instância do modelo Veiculo
        
    Returns:
        Decimal: Lucro calculado
    """
    return veiculo.valor_venda - veiculo.valor_compra - veiculo.total_despesas()


# ❌ RUIM
def calc(v):
    return v.vv - v.vc - v.td()
```

### HTML/Templates

```html
<!-- ✅ BOM -->
<div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-semibold mb-4">Título</h2>
    <p class="text-gray-600">Conteúdo</p>
</div>

<!-- ❌ RUIM -->
<div class="bg-white rounded-lg shadow p-6"><h2 class="text-xl font-semibold mb-4">Título</h2><p class="text-gray-600">Conteúdo</p></div>
```

## 🔍 Code Review

Todos os PRs passam por revisão. Esperamos:

- ✅ Código funcional e testado
- ✅ Sem conflitos com a branch main
- ✅ Documentação adequada
- ✅ Segue os padrões do projeto

## ❓ Dúvidas?

- Abra uma [issue](https://github.com/seu-usuario/gestao-veiculos/issues) com a tag `question`
- Entre em contato: seu-email@exemplo.com

## 📜 Código de Conduta

### Nossos Valores

- 🤝 **Respeito:** Trate todos com respeito e profissionalismo
- 🌈 **Inclusão:** Todos são bem-vindos, independente de background
- 🎯 **Foco:** Mantenha discussões construtivas e relevantes
- 🚀 **Colaboração:** Trabalhe em equipe para melhorar o projeto

### Comportamentos Inaceitáveis

- ❌ Linguagem ofensiva ou discriminatória
- ❌ Assédio de qualquer tipo
- ❌ Spam ou propaganda não relacionada
- ❌ Qualquer comportamento não profissional

## 🎉 Reconhecimento

Contribuidores serão reconhecidos:

- Na seção de **Contributors** do GitHub
- No arquivo **CONTRIBUTORS.md**
- Nos **release notes** quando aplicável

---

**Obrigado por contribuir! Juntos fazemos um projeto melhor! 🚀**
