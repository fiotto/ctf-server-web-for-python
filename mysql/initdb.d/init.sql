SET CHARSET UTF8;

DROP DATABASE IF EXISTS ctf_db;
CREATE DATABASE ctf_db;
USE ctf_db;
DROP TABLE IF EXISTS users;
 
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    job VARCHAR(30) NOT NULL,
    delete_flag BOOLEAN NOT NULL DEFAULT FALSE
)DEFAULT CHARACTER SET=utf8;
 
INSERT INTO users (first_name, last_name, job) 
    VALUES 
    ("太郎", "山田", "サーバーサイドエンジニア"),
    ("次郎", "鈴木", "フロントエンドエンジニア"),
    ("三郎", "田中", "インフラエンジニア"),
    ("花子", "佐藤", "デザイナー");
INSERT INTO users (first_name, last_name, job, delete_flag)
    VALUES ("一郎", "渡辺", "myctf{scf_sql_injection_flag}", TRUE); /* フラグ1つ目(同じテーブル) */

DROP TABLE IF EXISTS flag;

CREATE TABLE flag (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    flag VARCHAR(60) NOT NULL,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)DEFAULT CHARACTER SET=utf8;

INSERT INTO flag (flag)
    VALUES ("myctf{next_flag_[/var/ctf/flag.md]}"); /* フラグ2つ目(別のテーブル) */
