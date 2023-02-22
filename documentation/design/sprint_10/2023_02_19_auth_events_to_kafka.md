# Диаграммы отправки Wellcome Email новому пользователю

```mermaid
sequenceDiagram
    actor User
    
    User ->> Auth: Submits sign up form.
    Auth ->> Kafka: "User signed up" event.
    Kafka -->> Auth: 
    Auth -->> User: HTTP.OK
    rect grey
        Note over NotificationETL,Kafka: In the background.<br/>ETL gets the event.
        NotificationETL ->> Kafka: Get new events. 
        Kafka -->> NotificationETL: "User signed up" event.
        NotificationETL ->> RabbitMQ: Puts "User wellcome" posting.
    end
    rect grey       
        Note over Worker,RabbitMQ: In the background.<br/>Worker gets messages.
        Worker ->> RabbitMQ: Get new messages.
        RabbitMQ -->> Worker: "User wellcome" posting.
        Worker ->> User: Sends email with email confirmation link.
    end 
    User ->> Auth: Clicks email confirmation link.
    Auth ->> Auth: Validates email confirmation request.
    Auth -->> User: HTTP.OK 
```

![Диаграмма классов ETL для"Wellcome email" после регистрации пользователя](
https://plantuml-server.kkeisuke.dev/svg/TLBDYXD14BxtKvHxIf0idZm4b5rayPA3cCr9fAcTgKoQzC_GNTbrb83kLL_1TrWKSKNKL-Xv8sj-N0FYORgxwllgwwzg-YGnHjuv2npq1Qbxl257u90f6bHfQtoD4HrWmI4kkR44U4KfE3e0QoosMD40HoeOVMKF2GvVEKf9ECcy9dZuu02xaE8gXfqldmGR8bnj39DIR5Z4piuNnv0_vf_vK_i-VuFyIuxVsm_vQvVAD-rr_jB588cRzgq4d_Dj-wwzblEjV3qf_pXMgh2O4gmInQMfF9Mh-koIFCCR1N3VbDtAJKtTNcDZ0vPpA4t1eFRA1oQmj9PWnE1HNqWEZPLz9x9QHFQAV0aTNQbnA5qBFVTV0-SHVLg7w2ZsZCu2kThAyBL7HtD878UyriORrdg2EzveqRWq1Kq7pE6MT1qI6r-b2NLTJM7s64vJuukdv2cY_BiNpmR6IodQgpi_2sdcx_LTQvDHQWvZnRIlsCjwrzFHSd002sme7XtqToh-_e2ZQ4Mi-q7f8lYrYVAuJF3Q6h-Tz4PNpnVZ5V-RJfZD3fMLEf4vowlz3G00.svg
)