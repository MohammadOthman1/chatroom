const express = require("express");
const mysql = require("mysql2");
const cors = require("cors");
const { getConnection, closeConnection } = require("./db"); //gets the functions from db.js

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

app.listen(port, () => {
    console.log(`API is running on port ${port}`);
});

app.get("/", (req, res) => {
    res.send("Welcome to the server!");
});

async function checkUsername(username, connection){
    try{
        const query = "SELECT username FROM users WHERE username LIKE ?";
        const values = [`%${username}%`];
        const [result] = await connection.query(query, values);
        connection.release();  
        if (result.length > 0){
            return true;
        }
    }
    catch (err) {
        console.error("Error querying MySQL: ", err);
    };
};

async function checkEmail(email, connection){
    try{
        const query = "SELECT email FROM users WHERE email LIKE ?";
        const values = [`%${email}%`];
        const [result] = await connection.query(query, values)
        connection.release();
        if (result.length > 0){
            return true;
        }
    }
    catch (err) {
        console.error("Error querying Mysql: ", err);
    };

};

async function checkPassword(password, connection){
    try{
        const query = "SELECT password FROM users WHERE password LIKE ?";
        const values = [`%${password}%`];
        const [result] = await connection.query(query, values);
        connection.release();
        if (result.length > 0){
            return true;
        }
    }
    catch (err) {
        console.error("Error querying Mysql: ", err);
    };
};
async function checkLogin(username){
    try{
        const query = "SELECT password FROM users WHERE username LIKE ?";
        const values = [`%${username}%`];
        const [result] = await conenction.query(query, values);
        connection.release()
        if (result.length > 0){
            console.log("brbrbr ", result);
            return result;
        };

    }
    catch(err){
        console.error("Error querying Mysql: ",err);
    };
    
};
app.get("/sign-up", async (req, res) =>{
    const {username, email, password} = req.query;
    try{
        const connection = await getConnection();
        const usernameResult = await checkUsername(username, connection);
        if (usernameResult){
            res.send("This username is not available, Type another one");
            return;
        }
        const emailResult = await checkEmail(email, connection);
        if (emailResult){
            res.send("Email Already used");
            return;
        }
        const query = "INSERT INTO users (username, password, email, fk_rank) VALUES (?, ?, ?, ?)";
        const values = [username, password, email, 3];
        await connection.query(query, values);
        connection.release();
        res.send("User inserted succesfully");
        await closeConnection(connection);
    }
    catch (err) {
        console.error("Error querying MySQL: ", err);
        res.status(500).json({ error: "Internal server error" });
    }
});

app.get("/log-in", async (req, res) =>{
    const {username, password} = req.query;

    try{
        const connection = await getConnection();
        const check = checkLogin(username);
        if (!check){
            res.send("Username / password are wrong");
            return;
        }

        connection.release();
        await closeConnection(connection);
        res.send("Logged in succesfully");
        return true; //if client receives true then client.py should let him in 
    }
    catch (err){
        console.error("Error querying Mysql : ", err);
        res.status(500).json({error: "Internal server error"});
    }
})
