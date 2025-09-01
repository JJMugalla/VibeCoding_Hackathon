CREATE DATABASE IF NOT EXISTS polyglotpals;
USE polyglotpals;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subscription_status ENUM('free', 'premium') DEFAULT 'free',
    subscription_end_date DATE NULL
);

CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    language ENUM('english', 'spanish', 'swahili') NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    language ENUM('english', 'spanish', 'swahili') NOT NULL,
    level INT DEFAULT 1,
    points INT DEFAULT 0,
    last_activity DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_language (user_id, language)
);

--variables DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=polyglotpals
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
HF_API_TOKEN=your_hugging_face_token