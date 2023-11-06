const express = require("express");
const mysql = require("mysql2");
const cors = require("cors");
const { getConnection, closeConnection } = require("./db"); //gets the functions from db.js
const bcrypt = require("bcrypt");
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

async function generateHash(password) {
    try {
        const hash = await bcrypt.hash(password, 12);
        return hash;
    } catch (err) {
        console.error(err.message);
    }
}

async function checkUsername(username, connection){
    try{
        const query = "SELECT username FROM users WHERE username = ?";
        const values = [username];
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
        const query = "SELECT email FROM users WHERE email = ?";
        const values = [email];
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
        const query = "SELECT password FROM users WHERE password = ?";
        const values = [password];
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
async function checkLogin(username, connection){
    try{
        const query = "SELECT password FROM users WHERE username = ?";
        const values = [username];
        const [result] = await connection.query(query, values);
        connection.release()
        if (result.length > 0){
            return result;
        };
    }
    catch(err){
        console.error("Error querying Mysql: ",err);
    };
    
};
app.post("/sign-up", async (req, res) =>{
    const {username, email, password} = req.query;
    try{
        const connection = await getConnection();
        const usernameResult = await checkUsername(username, connection);
        if (usernameResult){
            res.send("username");
            return;
        }
        const emailResult = await checkEmail(email, connection);
        if (emailResult){
            res.send("email");
            return;
        }

        const hashedPwd = await generateHash(password);

        const query = "INSERT INTO users (username, password, email, fk_rank) VALUES (?, ?, ?, ?)";
        const values = [username, hashedPwd, email, 3];
        await connection.query(query, values);
        connection.release();

        res.send("success");
        await closeConnection(connection);
    }
    catch (err) {
        console.error("Error querying MySQL: ", err);
        res.status(500).json({ error: "Internal server error" });
    }
});

app.post("/log-in", async (req, res) =>{
    const {username, password} = req.query;
    try{
        const connection = await getConnection();
        const check = await checkLogin(username, connection);
        connection.release();
        if (!check){
            res.send("Username / password are wrong");
            return;
        }

        const getHash = check[0].password;
        bcrypt.compare(password, getHash, function(err, result) {
            if (err) {
                res.status(500).send('Error comparing passwords');
            }
            else if (result) {
                res.send("Success");
            }
            else {
                res.send("Username / password ");
            }
        });
        await closeConnection(connection); 
    }
    catch (err){
        console.error("Error querying Mysql : ", err);
        res.status(500).json({error: "Internal server error"});
    }
})


