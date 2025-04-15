-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 16 2025 г., 00:44
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `contract_management`
--

-- --------------------------------------------------------

--
-- Структура таблицы `agents`
--

CREATE TABLE `agents` (
  `id` int NOT NULL,
  `name` varchar(200) NOT NULL,
  `inn` varchar(20) DEFAULT NULL,
  `director_name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `agents`
--

INSERT INTO `agents` (`id`, `name`, `inn`, `director_name`, `phone`, `email`) VALUES
(1, 'ООО \"СтройТех\"', '7701234567', 'Козлов Андрей Викторович', '+79991234567', 'info@stroitech.ru'),
(2, 'ЗАО \"СтройМатериалы\"', '7707654321', 'Николаева Ольга Ивановна', '+79997654321', 'sales@stroymat.ru'),
(3, 'ИП Сергеев П.А.', '7712345678', 'Сергеев Павел Александрович', '+79992345678', 'sergeev.p@mail.ru');

-- --------------------------------------------------------

--
-- Структура таблицы `approval_processes`
--

CREATE TABLE `approval_processes` (
  `id` int NOT NULL,
  `contract_id` int DEFAULT NULL,
  `approver_id` int DEFAULT NULL,
  `status` varchar(20) DEFAULT 'В ожидании' COMMENT 'В ожидании, Одобрено, Отклонено',
  `comments` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `approval_processes`
--

INSERT INTO `approval_processes` (`id`, `contract_id`, `approver_id`, `status`, `comments`, `created_at`) VALUES
(4, 1, 3, 'Одобрено', 'Согласован без замечаний', '2025-04-15 18:02:49'),
(5, 3, 3, 'В ожидании', 'Ожидает проверки бухгалтерий', '2025-04-15 18:02:49'),
(6, 5, 3, 'В ожидании', 'на рассмотрении у менеджера', '2025-04-15 18:03:14');

-- --------------------------------------------------------

--
-- Структура таблицы `contracts`
--

CREATE TABLE `contracts` (
  `id` int NOT NULL,
  `contract_number` varchar(50) NOT NULL,
  `type_id` int DEFAULT NULL,
  `agent_id` int DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'Черновик' COMMENT 'Черновик, На согласовании, Активен, Завершен, Расторгнут',
  `created_by_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `contracts`
--

INSERT INTO `contracts` (`id`, `contract_number`, `type_id`, `agent_id`, `name`, `start_date`, `end_date`, `status`, `created_by_id`, `created_at`) VALUES
(1, 'ДГ-2025-001', 1, 1, 'Договор подряда на строительство офиса', '2025-04-08', '2025-05-05', 'Активен', 1, '2025-04-15 17:55:53'),
(3, 'ДГ-2025-003', 3, 3, 'Аренда строительной техники', '2025-04-09', '2025-05-10', 'Черновик', 1, '2025-04-15 17:55:53'),
(5, 'ДГ-2025-98', 4, 3, 'Аренда строительной техники', '2025-04-15', '2025-04-16', 'На согласовании', 2, '2025-04-15 18:01:37'),
(6, '8789', 4, 2, NULL, NULL, NULL, 'Черновик', 2, '2025-04-15 21:28:04'),
(7, '98888', 3, 2, NULL, NULL, NULL, 'Черновик', 2, '2025-04-15 21:29:54');

-- --------------------------------------------------------

--
-- Структура таблицы `contract_tasks`
--

CREATE TABLE `contract_tasks` (
  `id` int NOT NULL,
  `contract_id` int DEFAULT NULL,
  `title` varchar(200) NOT NULL,
  `assigned_to` int DEFAULT NULL,
  `deadline` date DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Новая' COMMENT 'Новая, В работе, Завершена, Отменена',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `contract_tasks`
--

INSERT INTO `contract_tasks` (`id`, `contract_id`, `title`, `assigned_to`, `deadline`, `status`, `created_at`) VALUES
(1, 1, 'Подготовить смету', 2, '2024-01-25', 'Завершена', '2025-04-15 17:55:53'),
(2, 1, 'Согласовать проект с заказчиком', 3, '2024-02-10', 'Завершена', '2025-04-15 17:55:53'),
(4, 3, 'Подготовить спецификацию техники', 2, '2024-03-20', 'Новая', '2025-04-15 17:55:53'),
(5, 5, 'Написать курсач', 2, '2025-04-20', 'Новая', '2025-04-15 21:28:53');

-- --------------------------------------------------------

--
-- Структура таблицы `contract_types`
--

CREATE TABLE `contract_types` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `contract_types`
--

INSERT INTO `contract_types` (`id`, `name`) VALUES
(3, 'Договор аренды'),
(4, 'Договор оказания услуг'),
(1, 'Договор подряда'),
(2, 'Договор поставки');

-- --------------------------------------------------------

--
-- Структура таблицы `notifications`
--

CREATE TABLE `notifications` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `message`, `is_read`, `created_at`) VALUES
(1, 2, 'У вас новая задача: Подготовить смету по договору ДГ-2024-001', 1, '2025-04-15 17:55:53'),
(2, 3, 'У вас новая задача: Согласовать проект с заказчиком по договору ДГ-2024-001', 1, '2025-04-15 17:55:53'),
(3, 3, 'Необходимо оформить заказ на материалы по договору ДГ-2024-002', 0, '2025-04-15 17:55:53');

-- --------------------------------------------------------

--
-- Структура таблицы `Users`
--

CREATE TABLE `Users` (
  `id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `passw` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'user' COMMENT 'user или manager'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Users`
--

INSERT INTO `Users` (`id`, `username`, `passw`, `full_name`, `email`, `role`) VALUES
(1, 'admin', 'admin', 'Администратор Системы', 'admin@company.com', 'manager'),
(2, 'user1', 'qwerty', 'Иванов Иван Иванович', 'user1@company.com', 'user'),
(3, 'user2', 'qazwsx', 'Петрова Мария Сергеевна', 'user2@company.com', 'user'),
(6, 'a', 'a', 'apal', 'apall', 'manager'),
(7, 'katya', 'katya', 'Беспалова Екатерина Беспаловна', 'katya@mail.ru', 'manager'),
(8, 'sasha', 'sasha', 'Трусов Александр Иванович', 'sasha@mail.ru', 'user');

-- --------------------------------------------------------

--
-- Структура таблицы `user_access`
--

CREATE TABLE `user_access` (
  `user_id` int NOT NULL,
  `contract_type_id` int NOT NULL,
  `has_access` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `user_access`
--

INSERT INTO `user_access` (`user_id`, `contract_type_id`, `has_access`) VALUES
(1, 1, 1),
(1, 2, 1),
(1, 3, 0),
(1, 4, 1),
(2, 1, 1),
(2, 2, 0),
(2, 3, 0),
(2, 4, 0),
(3, 1, 0),
(3, 2, 0),
(3, 3, 1),
(3, 4, 0),
(6, 1, 1),
(6, 2, 0),
(6, 3, 1),
(6, 4, 1),
(7, 1, 1),
(7, 2, 0),
(7, 3, 1),
(7, 4, 0),
(8, 1, 0),
(8, 2, 0),
(8, 3, 0),
(8, 4, 0);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `agents`
--
ALTER TABLE `agents`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `approval_processes`
--
ALTER TABLE `approval_processes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contract_id` (`contract_id`),
  ADD KEY `approver_id` (`approver_id`);

--
-- Индексы таблицы `contracts`
--
ALTER TABLE `contracts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `type_id` (`type_id`),
  ADD KEY `agent_id` (`agent_id`),
  ADD KEY `created_by_id` (`created_by_id`);

--
-- Индексы таблицы `contract_tasks`
--
ALTER TABLE `contract_tasks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contract_id` (`contract_id`),
  ADD KEY `assigned_to` (`assigned_to`);

--
-- Индексы таблицы `contract_types`
--
ALTER TABLE `contract_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Индексы таблицы `user_access`
--
ALTER TABLE `user_access`
  ADD PRIMARY KEY (`user_id`,`contract_type_id`),
  ADD KEY `contract_type_id` (`contract_type_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `agents`
--
ALTER TABLE `agents`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `approval_processes`
--
ALTER TABLE `approval_processes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `contracts`
--
ALTER TABLE `contracts`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `contract_tasks`
--
ALTER TABLE `contract_tasks`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `contract_types`
--
ALTER TABLE `contract_types`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `Users`
--
ALTER TABLE `Users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `approval_processes`
--
ALTER TABLE `approval_processes`
  ADD CONSTRAINT `approval_processes_ibfk_1` FOREIGN KEY (`contract_id`) REFERENCES `contracts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `approval_processes_ibfk_2` FOREIGN KEY (`approver_id`) REFERENCES `Users` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `contracts`
--
ALTER TABLE `contracts`
  ADD CONSTRAINT `contracts_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `contract_types` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `contracts_ibfk_2` FOREIGN KEY (`agent_id`) REFERENCES `agents` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `contracts_ibfk_3` FOREIGN KEY (`created_by_id`) REFERENCES `Users` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `contract_tasks`
--
ALTER TABLE `contract_tasks`
  ADD CONSTRAINT `contract_tasks_ibfk_1` FOREIGN KEY (`contract_id`) REFERENCES `contracts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `contract_tasks_ibfk_2` FOREIGN KEY (`assigned_to`) REFERENCES `Users` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `user_access`
--
ALTER TABLE `user_access`
  ADD CONSTRAINT `user_access_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_access_ibfk_2` FOREIGN KEY (`contract_type_id`) REFERENCES `contract_types` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
