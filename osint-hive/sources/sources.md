# Реестр источников

Статус у всех: `search` (страница не открыта, факты из поисковой выдачи). См. README.

## Первичка: госорганы

| ID | Источник | Дата | Что содержит | URL |
|----|----------|------|--------------|-----|
| S1 | DOJ OPA: «U.S. Department of Justice Disrupts Hive Ransomware Variant» | 2023-01-26 | Проникновение ФБР в сеть Hive с конца июля 2022; >1500 жертв в >80 странах; >300 ключей текущим жертвам и >1000 прошлым; предотвращено ~$130M выкупов; изъятие серверов вместе с ФРГ и нидерландской NHTCU. Имён и обвинительного заключения нет. | https://www.justice.gov/archives/opa/pr/us-department-justice-disrupts-hive-ransomware-variant |
| S2 | Речь генпрокурора Гарланда о Hive | 2023-01-26 | Сопровождение S1 | https://www.justice.gov/opa/speech/attorney-general-merrick-b-garland-delivers-remarks-disruption-hive-ransomware-variant |
| S3 | CISA/FBI/HHS AA22-321A «#StopRansomware: Hive» | 2022-11-17 | RaaS; >1300 компаний, ~$100M выкупов (на ноябрь 2022); вектор входа: RDP/VPN с однофакторной аутентификацией, CVE-2020-12812 (FortiOS, обход MFA), фишинг, Exchange CVE-2021-31207 / CVE-2021-34473 / CVE-2021-34523 (ProxyShell); повторные атаки на тех, кто восстановился без оплаты. Есть STIX с IOC. | https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-321a |
| S4 | Тот же адвайзори, PDF на IC3 | 2022-11-17 | Копия S3 | https://www.ic3.gov/CSA/2022/221117.pdf |
| S5 | DOJ USAO-NJ: обвинение Матвееву | 2023-05-16 | Обвинение в D.N.J.: конспирация с LockBit, Babuk, Hive; Hive-эпизод: ~2022-05-27, некоммерческая организация поведенческого здоровья, округ Мерсер, Нью-Джерси. Алиасы: Wazawaka, m1x, Boriselcin, Uhodiransomwar. | https://www.justice.gov/usao-nj/pr/russian-national-charged-ransomware-attacks-against-critical-infrastructure |
| S6 | Обвинительное заключение Матвеева (PDF) | подано 2022-12, раскрыто 2023-05 | Текст обвинения | https://www.justice.gov/d9/2023-05/matveev.indictment.pdf |
| S7 | FBI Wanted: Mikhail Pavlovich Matveev | — | Ориентировка | https://www.fbi.gov/wanted/cyber/mikhail-pavlovich-matveev/download.pdf |
| S8 | State Dept / RFJ: награда за лидеров Hive | 2024-02-08 | До $10M за идентификацию/местонахождение лидеров; до $5M за арест/осуждение любого участника. Сам текст state.gov в выдаче не найден, есть только перепечатки (S20, S21). | искать на state.gov / rewardsforjustice.net |

## Вторичка: СМИ и вендоры

| ID | Источник | Дата | Что содержит | URL |
|----|----------|------|--------------|-----|
| S10 | TechCrunch: изъятие портала Hive | 2023-01-26 | Баннер изъятия; DOJ, FBI, Secret Service, европейские ведомства | https://techcrunch.com/2023/01/26/united-states-hive-ransomware-seized |
| S11 | Microsoft Security Blog: Hive на Rust | 2022 | Ранние версии на Go, новая на Rust; шифрование строк | https://www.microsoft.com/en-us/security/blog/?p=117287 |
| S12 | Bitdefender: «Hive ransomware's offspring: Hunters International» | 2023 (Q4) | Пересечение кода Hive и Hunters; вывод, что лидеры Hive передали активы Hunters International; упор Hunters на кражу данных | https://businessinsights.bitdefender.com/hive-ransomwares-offspring-hunters-international-takes-the-stage |
| S13 | BleepingComputer: Hunters International, возможный ребренд Hive | 2023 (Q4) | Пересечение кода ≥60% (Will Thomas @BushidoToken); rivitna: образец соответствует Hive v6; Hunters утверждают, что купили исходники и сайт | https://www.bleepingcomputer.com/news/security/new-hunters-international-ransomware-possible-rebrand-of-hive/ |
| S14 | BleepingComputer: арест в Париже | 2023-12 | Россиянин ~40 лет, живёт на Кипре; задержан 5 дек 2023; изъято >€570k в крипте; связан с кошельками через активность в соцсетях | https://www.bleepingcomputer.com/news/security/french-police-arrests-russian-suspect-linked-to-hive-ransomware/ |
| S15 | Security Affairs: арест в Париже | 2023-12 | То же; Europol + Eurojust | https://securityaffairs.com/155815/cyber-crime/french-authorities-hive-ransomware-member.html |
| S16 | ForkLog: арест в Париже | 2023-12 | Называет задержанного «оператором» Hive. Расходится с S14/S15 («отмыватель») | https://forklog.com/en/alleged-hive-ransomware-operator-arrested-in-france/amp |
| S17 | TechCrunch: Europol, Украина | 2023-11-28 | 5 арестов, «главарь» 32 лет, 30 обысков; группа использовала Hive, LockerGoga, MegaCortex, Dharma (аффилиат, не ядро Hive) | https://techcrunch.com/2023/11/28/europol-hackers-ransomware-lockergoga-hive/ |
| S18 | The Register: Hunters International закрывается | 2025-07-03 | Закрытие, бесплатные декрипторы, удаление сайта утечек | https://www.theregister.com/2025/07/03/hunters_international_shutdown/ |
| S19 | Infosecurity Magazine: Hunters не закрывается, а ребрендится | 2025-04 | Анализ Group-IB: World Leaks запущен 2025-01-01, только кража данных; инструмент кражи («Storage Software»); операторы других групп называют RaaS «Hive» | https://infosecurity-magazine.com/news/ransomware-hunters-international |
| S20 | The Record: награда $10M за Hive | 2024-02-08 | Детали награды | https://therecord.media/us-offers-10-million-dollar-reward-for-hive-ransomware-info |
| S21 | The Hacker News: награда за Hive | 2024-02 | То же | https://thehackernews.com/2024/02/us-offers-10-million-bounty-for-info.html |
| S22 | The Record: Матвеев под санкциями и обвинён | 2023-05-16 | OFAC SDN; в записи SDN нет криптоадресов | https://therecord.media/alleged-babuk-ransomware-leader-sanctioned-and-indicted-by-us |
| S23 | KrebsOnSecurity: Россия арестовала Матвеева | 2024-12-04 | Арест в РФ; ч.1 ст.273 УК РФ; дело в Центральном райсуде Калининграда | https://krebsonsecurity.com/2024/12/u-s-offered-10m-for-hacker-just-arrested-by-russia/ |
| S24 | CyberScoop: обвинение Матвееву в РФ | 2024-11 | То же; по словам исследователя, на свободе под залогом | https://cyberscoop.com/mikhail-matveev-wazawaka-russia-charges/ |
| S25 | Wikipedia: Hive (ransomware) | — | Сводка; использовать только как указатель на первичку | https://en.wikipedia.org/wiki/Hive_(ransomware) |
| S26 | Trend Micro: Ransomware Spotlight Hive | 2022 | TTP, профиль жертв | https://www.trendmicro.com/vinfo/us/security/news/ransomware-spotlight/ransomware-spotlight-hive |
| S27 | Varonis: Hive Ransomware Analysis | 2022 | Разбор инцидента: вход через ProxyShell | https://varonis.com/blog/hive-ransomware-analysis |

## Пробелы в первичке

- Полный текст AA22-321A и STIX-пакет (IOC: адреса, хеши, onion-домены, контакты) не получены.
- Оригинал объявления state.gov / RFJ от 2024-02-08 не найден.
- Официального пресс-релиза Police nationale / OFAC (Франция) по аресту в Париже нет; есть только СМИ.
- Публичных отчётов о трассировке кошельков Hive (Chainalysis, Elliptic, TRM) в выдаче нет.
