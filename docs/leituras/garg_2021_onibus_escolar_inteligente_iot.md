# Guia de leitura: sistema de segurança para ônibus escolar com IoT (Garg *et al.*, 2021)

> **Guia de estudo em português**, não é tradução. O artigo não traz licença aberta, então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** GARG, B.; JOB, A.; JAKARWAR, V.; JHA, N. IoT based smart school bus security system. *Turkish Online Journal of Qualitative Inquiry (TOJQI)*, v. 12, n. 4, p. 1251–1260, abr. 2021.
> **PDF local:** `Downloads/Referencias/garg_2021_onibus_escolar_inteligente_iot.pdf`
>
> **Correção para o documento de lacunas:** o [documento de lacunas](../lacunas_revisao_bibliografica.md) registra este trabalho como "*IoT-Based Smart School Bus Security System*, 2023", encontrado só no ResearchGate. O PDF mostra que ele foi publicado na TOJQI em 2021, com os autores acima.

---

## Em uma frase

Um sistema para ônibus escolar que registra o embarque e o desembarque dos alunos por **cartão RFID**, confirma a identidade com **reconhecimento facial em uma câmera ESP32-CAM** e avisa os pais por SMS ou e-mail.

## O sistema

1. **RFID:** cada aluno tem uma etiqueta; um leitor RFID ligado a um Arduino e a um computador registra as passagens.
2. **Câmera:** um módulo ESP32-CAM (microcontrolador ESP32 com câmera OV2640, Wi-Fi e Bluetooth) captura o rosto de quem embarca. O reconhecimento usa Python e OpenCV, para conferir se quem passou o cartão é mesmo o aluno.
3. **Software:** mostra as leituras em tempo real, cadastra etiquetas e guarda o histórico de entradas e saídas.
4. **Avisos:** quando o aluno entra ou sai do ônibus, os pais recebem SMS ou e-mail.
5. O artigo também cita trabalhos com GPS para mostrar a localização do ônibus.

## Resultados

- O artigo é descritivo: afirma que o sistema detecta e identifica os alunos no embarque e no desembarque, confere se o aluno desce no ponto certo e dispensa intervenção humana.
- **Não há avaliação quantitativa** (acurácia, tempo, testes com usuários).

## Limitações

- Sem medições, não dá para saber quão bem o reconhecimento funciona.
- Não fica claro onde o reconhecimento é processado: o ESP32-CAM tem pouca memória para modelos profundos, então provavelmente as imagens vão para um computador.
- RFID exige que o aluno lembre do cartão, e o cartão pode ser usado por outra pessoa; o rosto entra só como conferência.
- Não discute privacidade das imagens de crianças.

## Ligação com o TCC

- É o **trabalho correlato mais próximo do tema** (presença em ônibus escolar com aviso aos pais) e o único da pasta com **ESP32**. Serve para a seção de trabalhos relacionados da monografia e para a análise de trade-off Raspberry Pi × ESP32 da Atividade 1.3 (item A2 do [documento de lacunas](../lacunas_revisao_bibliografica.md)).
- Diferenças a destacar na comparação: o projeto não exige cartão nem ação do aluno; faz o reconhecimento no próprio dispositivo; funciona sem rede, com fila local; e não guarda imagens.
- Já está entre as referências candidatas da Visão Geral (comentário `% CITAR:` em `visao_geral.tex`); ao citar, use os dados de 2021 desta publicação.

## Perguntas para conferir a leitura

1. Qual o papel do RFID e qual o papel do reconhecimento facial nesse sistema?
2. Por que é improvável que o ESP32-CAM rode sozinho um modelo como o ArcFace?
3. Quais quatro diferenças do projeto em relação a este sistema valem destacar na monografia?
