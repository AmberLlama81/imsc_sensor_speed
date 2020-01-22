const pg = require("pg").Pool;

const pool = new pg({
    host: 'gd.usc.edu',
    port: 5433,
    database: 'adms',
    user: 'adms-api',
    password: 'V^YDiwdR&VvM',
})

const getSpeeds = (request, response) => {
    pool.query(`SELECT speed FROM congestion.congestion_data LIMIT 10`, (error, results) => {
        if (error) {
            throw error
        }
        response.status(200).json(results.rows)
    })
}

const getRecentSpeed = (request, response) => {
    pool.query('SELECT speed FROM congestion.congestion_data ORDER BY date_and_time DESC LIMIT 1', (error, results) => {
        if (error) {
            throw error
        }
        response.status(200).json(results.rows)
    })
}

const getRecentSpeed2 = (request, response) => {
    pool.query('SELECT max(date_and_time) FROM congestion.congestion_data', (error, firstResults) => {
        if (error) {
            throw error
        }
        pool.query('SELECT speed FROM congestion.congestion_data WHERE date_and_time = $1', firstResults.rows["max"], (error, results) => {
            if (error) {
                throw error
            }
            response.status(200).json(results.rows)
        })
    })
}

const getNextStop = (request, response) => {
    pool.query('SELECT * FROM transit.bus_data LIMIT 1', (error, results) => {
        if (error) {
            throw error
        }
        response.status(200).json(results.rows)
    })
} 

const getSpeedById = (request, response) => {
    const id = parseInt(request.params.id)

    pool.query('SELECT speed FROM congestion.congestion_data WHERE link_id = $1', [id], (error, results) => {
        if (error) {
            throw error
        }
        response.status(200).json(results.rows)
    })
}

module.exports = {
    getSpeeds,
    getRecentSpeed,
    getRecentSpeed2,
    getNextStop,
    getSpeedById,
}
