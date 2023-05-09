# BookTracker

Sobre o projeto Book Tracker

O objetivo desse projeto é construir uma aplicação que faz a gestão de uma biblioteca.

Principais Funcionalidades:

# Usuários

O sistema permite o cadastro de 3 tipos de usários:

<strong> Admin </strong>: tem acesso a todas as funcionalidades do aplicativo

<strong> Colaborador </strong> – é responsável por:
a. Cadastrar novos livros
b. Emprestar e devolver livros
c. Verificar o histórico de empréstimos de cada estudante
d. Verificar status do estudante (se está bloqueado ou pode fazer empréstimos)

<strong> Estudante </strong> – é responsável por:
a. Visualizar seu próprio histórico de livros emprestados
b. Obter informação de qualquer livro
c. "Seguir" um livro a fim de receber notificações no e-mail conforme a disponibilidade/status do livro.

<strong>OBS</strong>: qualquer pessoa poderá visualizar informações dos livros sem ter necessariamente uma conta criada.

# Regras de negócio:

## Empréstimos

• Cada livro só poderá ser emprestado por um período máximo de 14 dias;

• Quando é realizado um empréstimo, é automaticamente gerada uma data de retorno do livro, que é armazenada na chave loan_estimate_return. Caso a data corresponda a um sábado, domingo ou feriado, a data estimada de devolução será automaticamente o próximo dia útil.

• Quando o usuário devolve um livro atrasado, ou seja, numa data posterior à data estimada de retorno (loan_estimate_return), o usuário é automaticamente bloqueado para novos empréstimos por um período de 7 dias, a partir da data em que devolveu efetivamente o livro. O bloqueio do usuário é controlado por uma chave denominada cleared_date, na conta do usuário, que informa a data a partir da qual um usuário está desbloqueado (essa data tem como valor inicial a data de criação da conta do usuário). Dessa forma, em caso de bloqueio, essa chave conterá uma data futura.

• Cada estudante poderá pegar emprestado no máximo 5 livros simultaneamente. Quando atinge esse número, até que devolva algum livro que tomou emprestado, não poderá solicitar novo empréstimo. Uma chave number_loans na conta de cada usuário controle a quantidade de empréstimos do usuário.

## Usuários:

Estudante: pode criar sua própria conta;

Colaborador: como funcionário, só pode ser criado por um usuário admin;

Admin: pode criar colaboradores e admins. O primeiro admin do sistema será criado pelo terminal através do comando:

python manage.py create_admin -u <username> -p <password> -e <email>.
OU
python manage.py create_admin --username <username> --password <password> --email <email>.

Caso não informe nenhum atributo no comando acima, o usuário é criado com os seguintes campos:
• Username: admin
• Email: <username>@booktracker.com
• Password: admin1234

## Livros

Um livro é criado por uma colaborador ou administrador. Quando da criação, deverão ser informados os dados do livro, bem como os códigos de classificação das cópias disponíveis (classification_code), a categoria e a editor. É obrigatório informar pelo menos uma cópia no cadastro inicial do livro.

É possível fazer um soft delete de uma cópia, bem como adicionar novas cópias a um livro existente.

## Seguidores

Um estudante pode seguir um livro. Somente ele mesmo poderá deixar de seguir um livro. Para isso, precisará estar logado em sua conta. Ao seguir um livro, será informado por email sempre que uma cópia desse livro estiver disponível para empréstimo. Enquanto estiver seguindo um livro, receberá este e-mail.

## Notificações de usuários

Além de ser notificado por email quando uma cópia do livro que estiver seguindo fica disponível, o estudante será notificado por e-mail nas seguintes condições:

- Na véspera da data de devolução do livro;
- Quando não tiver devolvido o livro na data prevista.

# Documentação das rotas

https://web-production-aadc0.up.railway.app/api/docs/redoc/
