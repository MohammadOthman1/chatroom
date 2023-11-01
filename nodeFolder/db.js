const mysql = require("mysql2/promise");
require("dotenv").config();
const pool = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_DATABASE,
});

const getConnection = async () => {
    try{
        const connection = await pool.getConnection();
        return connection;
    }
    catch (error){
        console.error("Error Conencting to mysql: ", error);
    }
};

function closeConnection(connection){
    return connection.release();
};

module.exports = {
    getConnection,
    closeConnection,
}
