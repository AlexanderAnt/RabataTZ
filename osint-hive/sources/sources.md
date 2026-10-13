# Реестр источников

Статусы:
- `primary` — страница открыта 2026-10-13, копия лежит рядом (файл указан в колонке «Копия»), факты сверены с текстом.
- `search` — страница не открыта, факты из поисковой выдачи.

## Первичка: госорганы

| ID | Источник | Дата | Что содержит | URL | Статус / копия |
|----|----------|------|--------------|-----|----------------|
| S1 | DOJ OPA: «U.S. Department of Justice Disrupts Hive Ransomware Variant» | 2023-01-26 | Проникновение ФБР в сеть Hive с конца июля 2022; >1500 жертв в >80 странах, >$100M выплат с июня 2021; >300 ключей текущим жертвам и >1000 прошлым; предотвращено ~$130M. Модель RaaS, деление 80/20 (аффилиат/админы). Следствие: ФБР Тампа (Orlando RA), прокуратура Среднего округа Флориды + CCIPS. Изъятие с BKA, полицией Ройтлингена и нидерландской NHTCU. Имён нет. | https://www.justice.gov/archives/opa/pr/us-department-justice-disrupts-hive-ransomware-variant | `primary` · S1_doj_hive_2023-01-26.txt |
| S2 | Речь генпрокурора Гарланда о Hive | 2023-01-26 | Сопровождение S1 | https://www.justice.gov/opa/speech/attorney-general-merrick-b-garland-delivers-remarks-disruption-hive-ransomware-variant | `primary` · S2_garland_remarks.txt |
| S3 | CISA/FBI/HHS AA22-321A «#StopRansomware: Hive» | 2022-11-17 | RaaS; >1300 компаний, ~$100M выкупов (на ноябрь 2022); вектор входа: RDP/VPN с однофакторной аутентификацией, CVE-2020-12812 (FortiOS, обход MFA), фишинг, Exchange CVE-2021-31207 / CVE-2021-34473 / CVE-2021-34523 (ProxyShell), CVE-2021-42321. Записка HOW_TO_DECRYPT.txt, ключ *.key в корне, чат «sales department» в Tor, сайт утечек HiveLeaks, оплата в BTC. IOC: 4 домена .pw, 24 IP, 2 URL. Кошельков, почт и хешей в публичном пакете нет. | https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-321a | `primary` · S3_cisa_aa22-321a.txt, S3_AA22-321A.stix.xml |
| S4 | Тот же адвайзори, PDF на IC3 | 2022-11-17 | Копия S3 | https://www.ic3.gov/CSA/2022/221117.pdf | `primary` · S4_ic3_221117.pdf/.txt |
| S5 | DOJ USAO-NJ: обвинение Матвееву | 2023-05-16 | Обвинение в D.N.J. (с 2020 года): LockBit, Babuk, Hive. В пресс-релизе Hive-эпизод «Matveev and his Hive coconspirators» 2022-05-27 (Мерсер, NJ); в самом обвинении он сформулирован иначе (см. S6). Hive: >1400 жертв, до $120M выплат. OFAC SDN + награда $10M. Подсказки: tips.fbi.gov / RewardsForJustice.net. Алиасы: Wazawaka, m1x, Boriselcin, Uhodiransomwar. | https://www.justice.gov/usao-nj/pr/russian-national-charged-ransomware-attacks-against-critical-infrastructure | `primary` · S5_doj_matveev.txt |
| S6 | Обвинительное заключение Матвеева (PDF) | подано 2022-12, раскрыто 2023-05 | Count 5 (ст.371, Hive, с июня 2021): атака 2022-05-27 на Hive-Victim-1 (Мерсер, NJ) вменена «Hive Coconspirators» без Матвеева; 2022-06-02 Hive-Victim-2 (Сомерсет, NJ) — «MATVEEV and the Hive Coconspirators» + цитата записки с выкупом. Count 6: повреждение компьютера Hive-Victim-2. Hive: ≈1400 атак, ≥$270M требований, до $120M выплат | https://www.justice.gov/d9/2023-05/matveev.indictment.pdf | `primary` · S6_matveev_indictment.pdf/.txt |
| S7 | FBI Wanted: Mikhail Pavlovich Matveev | — | Ориентировка | https://www.fbi.gov/wanted/cyber/mikhail-pavlovich-matveev/download.pdf | `primary` · S7_fbi_wanted_matveev.pdf/.txt |
| S8 | State Dept / RFJ: награда за лидеров Hive | 2024-02-08 | До $10M за идентификацию/местонахождение лидеров; до $5M за арест/осуждение любого участника. Сам текст state.gov в выдаче не найден, есть только перепечатки (S20, S21). | искать на state.gov / rewardsforjustice.net | `search` |

## Вторичка: СМИ и вендоры

| ID | Источник | Дата | Что содержит | URL | Статус / копия |
|----|----------|------|--------------|-----|----------------|
| S10 | TechCrunch: изъятие портала Hive | 2023-01-26 | Баннер изъятия; DOJ, FBI, Secret Service, европейские ведомства | https://techcrunch.com/2023/01/26/united-states-hive-ransomware-seized | `search` |
| S11 | Microsoft Security Blog: Hive на Rust | 2022 | Ранние версии на Go, новая на Rust; шифрование строк | https://www.microsoft.com/en-us/security/blog/?p=117287 | `search` |
| S12 | Bitdefender: «Hive ransomware's offspring: Hunters International» | 2023 (Q4) | Ссылается на ≥60% совпадения кода (чужое исследование). Пишет, что «похоже, лидеры Hive решили прекратить работу и передать активы Hunters International», и при этом считает правдоподобным заявление Hunters о покупке кода. Признаки заимствования кода (добавлен логгинг), Rust, параметры командной строки сокращены до пяти, ключ хранится внутри файлов | https://businessinsights.bitdefender.com/hive-ransomwares-offspring-hunters-international-takes-the-stage | `primary` · S12_bitdefender_hunters.txt |
| S13 | BleepingComputer: Hunters International, возможный ребренд Hive | 2023 (Q4) | Пересечение кода ≥60% (Will Thomas @BushidoToken); rivitna: образец соответствует Hive v6; Hunters утверждают, что купили исходники и сайт | https://www.bleepingcomputer.com/news/security/new-hunters-international-ransomware-possible-rebrand-of-hive/ | `primary` · S13_bleeping_hunters.txt |
| S14 | BleepingComputer: арест в Париже | 2023-12 | Россиянин 40 лет, живёт на Кипре; задержан 2023-12-05 в Париже; подозревается в отмывании выкупов; OFAC (французское Office anti-cybercriminalité) вышло на него через кошельки и активность в соцсетях; изъято €570k в крипте; обыск на Кипре; 2023-12-09 передан в профильную прокуратуру Парижа. Также: на серверах Hive найдены данные о 250 аффилиатах | https://www.bleepingcomputer.com/news/security/french-police-arrests-russian-suspect-linked-to-hive-ransomware/ | `primary` · S14_bleeping_paris.txt |
| S15 | Security Affairs: арест в Париже | 2023-12 | То же; Europol + Eurojust | https://securityaffairs.com/155815/cyber-crime/french-authorities-hive-ransomware-member.html | `search` |
| S16 | ForkLog: арест в Париже | 2023-12 | Называет задержанного «оператором» Hive. Расходится с S14/S15 («отмыватель») | https://forklog.com/en/alleged-hive-ransomware-operator-arrested-in-france/amp | `search` |
| S17 | TechCrunch: Europol, Украина | 2023-11-28 | 5 арестов, «главарь» 32 лет, 30 обысков; группа использовала Hive, LockerGoga, MegaCortex, Dharma (аффилиат, не ядро Hive) | https://techcrunch.com/2023/11/28/europol-hackers-ransomware-lockergoga-hive/ | `search` |
| S18 | The Register: Hunters International закрывается | 2025-07-03 | Закрытие, бесплатные декрипторы, удаление сайта утечек | https://www.theregister.com/2025/07/03/hunters_international_shutdown/ | `search` |
| S19 | Infosecurity Magazine: Hunters не закрывается, а ребрендится | 2025-04 | Анализ Group-IB: World Leaks запущен 2025-01-01, только кража данных; инструмент кражи («Storage Software»); операторы других групп называют RaaS «Hive» | https://infosecurity-magazine.com/news/ransomware-hunters-international | `search` |
| S20 | The Record: награда $10M за Hive | 2024-02-08 | Цитирует Госдеп: $10M за «key leadership positions», $5M за арест/осуждение любого участника; TOCRP. Парижский задержанный, по данным полиции, — «банкир» аффилиатов. Chainalysis: инфильтрация предотвратила ≥$210.4M | https://therecord.media/us-offers-10-million-dollar-reward-for-hive-ransomware-info | `primary` · S20_record_reward.txt |
| S21 | The Hacker News: награда за Hive | 2024-02 | То же | https://thehackernews.com/2024/02/us-offers-10-million-bounty-for-info.html | `search` |
| S22 | The Record: Матвеев под санкциями и обвинён | 2023-05-16 | OFAC SDN; в записи SDN нет криптоадресов | https://therecord.media/alleged-babuk-ransomware-leader-sanctioned-and-indicted-by-us | `search` |
| S23 | KrebsOnSecurity: Россия арестовала Матвеева | 2024-12-04 | Арест в РФ; ч.1 ст.273 УК РФ; дело в Центральном райсуде Калининграда | https://krebsonsecurity.com/2024/12/u-s-offered-10m-for-hacker-just-arrested-by-russia/ | `search` |
| S24 | CyberScoop: обвинение Матвееву в РФ | 2024-11 | То же; по словам исследователя, на свободе под залогом | https://cyberscoop.com/mikhail-matveev-wazawaka-russia-charges/ | `search` |
| S25 | Wikipedia: Hive (ransomware) | — | Сводка; использовать только как указатель на первичку | https://en.wikipedia.org/wiki/Hive_(ransomware) | `search` |
| S26 | Trend Micro: Ransomware Spotlight Hive | 2022 | TTP, профиль жертв | https://www.trendmicro.com/vinfo/us/security/news/ransomware-spotlight/ransomware-spotlight-hive | `search` |
| S27 | Varonis: Hive Ransomware Analysis | 2022 | Разбор инцидента: вход через ProxyShell | https://varonis.com/blog/hive-ransomware-analysis | `search` |

## Пробелы в первичке

- Оригинал объявления state.gov / RFJ от 2024-02-08 не найден.
- Официального пресс-релиза Police nationale / OFAC (Франция) по аресту в Париже нет; есть только СМИ.
- Публичных отчётов о трассировке кошельков Hive (Chainalysis, Elliptic, TRM) в выдаче нет.
