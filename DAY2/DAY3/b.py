from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from fastapi.responses import HTMLResponse


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="Hospital Support Request System",
    version="1.0.0"
)


# =========================================================
# DATABASE
# =========================================================

URL = "mongodb://127.0.0.1:27017"

client = MongoClient(URL)

db = client["hospital_support_db"]

service_requests = db["service_requests"]


# =========================================================
# SCHEMA
# =========================================================

class ServiceRequest(BaseModel):
    title: str
    description: str
    department: str
    status: str
    assigned_to: str


# =========================================================
# HELPER
# =========================================================

def request_helper(doc):

    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "description": doc["description"],
        "department": doc["department"],
        "status": doc["status"],
        "assigned_to": doc["assigned_to"]
    }


# =========================================================
# HOME PAGE
# =========================================================

@app.get("/", response_class=HTMLResponse)
def home():

    return """
<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Hospital Support Request System</title>


    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }


        body {

            font-family:
                Arial,
                Helvetica,
                sans-serif;

            background: #f5f9ff;

            color: #172554;

            overflow-x: hidden;
        }


        /* =================================================
           NAVBAR
        ================================================= */

        nav {

            height: 75px;

            display: flex;

            align-items: center;

            justify-content: space-between;

            padding: 0 7%;

            background:
                linear-gradient(
                    135deg,
                    #075985,
                    #2563eb,
                    #4f46e5
                );

            color: white;

            box-shadow:
                0 5px 25px rgba(37, 99, 235, 0.25);

            position: sticky;

            top: 0;

            z-index: 100;
        }


        .logo {

            display: flex;

            align-items: center;

            gap: 12px;

            font-size: 21px;

            font-weight: bold;
        }


        .logo-icon {

            width: 43px;

            height: 43px;

            background: white;

            color: #2563eb;

            border-radius: 13px;

            display: flex;

            align-items: center;

            justify-content: center;

            font-size: 25px;
        }


        .nav-links {

            display: flex;

            gap: 30px;

            align-items: center;
        }


        .nav-links a {

            color: white;

            text-decoration: none;

            font-size: 15px;

            font-weight: 600;

            opacity: 0.9;

            transition: 0.3s;
        }


        .nav-links a:hover {

            opacity: 1;

            transform: translateY(-2px);
        }


        /* =================================================
           HERO
        ================================================= */

        .hero {

            min-height: 560px;

            padding: 65px 7%;

            display: flex;

            align-items: center;

            gap: 50px;

            background:
                linear-gradient(
                    120deg,
                    #eff6ff,
                    #ffffff
                );
        }


        .hero-content {

            width: 50%;

            animation: slideLeft 0.8s ease;
        }


        .small-title {

            color: #2563eb;

            font-weight: bold;

            letter-spacing: 3px;

            font-size: 14px;

            margin-bottom: 18px;
        }


        .hero h1 {

            font-size: 55px;

            line-height: 1.1;

            margin-bottom: 22px;

            color: #172554;
        }


        .hero h1 span {

            color: #2563eb;
        }


        .hero p {

            font-size: 18px;

            line-height: 1.7;

            color: #64748b;

            max-width: 570px;

            margin-bottom: 30px;
        }


        .buttons {

            display: flex;

            gap: 15px;

            flex-wrap: wrap;
        }


        .primary-btn,
        .secondary-btn {

            padding: 15px 25px;

            border-radius: 12px;

            text-decoration: none;

            font-weight: bold;

            transition: 0.3s;

            display: inline-block;
        }


        .primary-btn {

            background:
                linear-gradient(
                    135deg,
                    #2563eb,
                    #4f46e5
                );

            color: white;

            box-shadow:
                0 10px 25px rgba(37, 99, 235, 0.25);
        }


        .secondary-btn {

            background: white;

            color: #2563eb;

            border: 2px solid #2563eb;
        }


        .primary-btn:hover,
        .secondary-btn:hover {

            transform: translateY(-3px);
        }


        /* =================================================
           HOSPITAL IMAGE
        ================================================= */

        .hero-image {

            width: 50%;

            height: 390px;

            border-radius: 30px;

            overflow: hidden;

            position: relative;

            box-shadow:
                0 25px 50px rgba(15, 23, 42, 0.2);

            animation: slideRight 0.8s ease;
        }


        .hero-image img {

            width: 100%;

            height: 100%;

            object-fit: cover;

            transition: transform 0.6s ease;
        }


        .hero-image:hover img {

            transform: scale(1.05);
        }


        .image-overlay {

            position: absolute;

            bottom: 0;

            left: 0;

            right: 0;

            padding: 25px;

            color: white;

            background:
                linear-gradient(
                    transparent,
                    rgba(15, 23, 42, 0.8)
                );
        }


        .image-overlay h3 {

            font-size: 22px;

            margin-bottom: 5px;
        }


        .image-overlay p {

            color: white;

            font-size: 14px;

            margin: 0;
        }


        /* =================================================
           SECTION
        ================================================= */

        .section {

            padding: 70px 7%;

            background: white;
        }


        .section-heading {

            text-align: center;

            margin-bottom: 45px;
        }


        .section-heading h2 {

            font-size: 35px;

            color: #172554;

            margin-bottom: 10px;
        }


        .section-heading p {

            color: #64748b;

            font-size: 16px;
        }


        /* =================================================
           CARDS
        ================================================= */

        .cards {

            display: grid;

            grid-template-columns:
                repeat(4, 1fr);

            gap: 22px;
        }


        .card {

            padding: 32px 25px;

            border-radius: 22px;

            text-align: center;

            transition:
                transform 0.3s,
                box-shadow 0.3s;

            border: 1px solid #e2e8f0;

            background: white;
        }


        .card:hover {

            transform: translateY(-10px);

            box-shadow:
                0 20px 40px rgba(15, 23, 42, 0.12);
        }


        .card-icon {

            width: 65px;

            height: 65px;

            margin: auto;

            margin-bottom: 20px;

            border-radius: 18px;

            display: flex;

            align-items: center;

            justify-content: center;

            font-size: 30px;
        }


        .green {

            background: #dcfce7;

            color: #16a34a;
        }


        .blue {

            background: #dbeafe;

            color: #2563eb;
        }


        .orange {

            background: #ffedd5;

            color: #ea580c;
        }


        .red {

            background: #fee2e2;

            color: #dc2626;
        }


        .card h3 {

            font-size: 20px;

            margin-bottom: 10px;

            color: #172554;
        }


        .card p {

            color: #64748b;

            line-height: 1.6;

            font-size: 14px;

            margin-bottom: 20px;
        }


        .card-button {

            display: inline-block;

            padding: 10px 18px;

            border-radius: 9px;

            color: white;

            text-decoration: none;

            font-size: 13px;

            font-weight: bold;
        }


        .green-button {

            background: #16a34a;
        }


        .blue-button {

            background: #2563eb;
        }


        .orange-button {

            background: #ea580c;
        }


        .red-button {

            background: #dc2626;
        }


        /* =================================================
           FEATURES
        ================================================= */

        .features {

            padding: 55px 7%;

            background:
                linear-gradient(
                    135deg,
                    #eff6ff,
                    #eef2ff
                );

            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 25px;
        }


        .feature {

            background: white;

            border-radius: 18px;

            padding: 28px;

            display: flex;

            align-items: center;

            gap: 18px;

            box-shadow:
                0 8px 25px rgba(15, 23, 42, 0.06);
        }


        .feature-icon {

            width: 55px;

            height: 55px;

            min-width: 55px;

            border-radius: 15px;

            background: #dbeafe;

            display: flex;

            align-items: center;

            justify-content: center;

            font-size: 25px;
        }


        .feature h3 {

            color: #172554;

            margin-bottom: 5px;

            font-size: 17px;
        }


        .feature p {

            color: #64748b;

            font-size: 13px;
        }


        /* =================================================
           FOOTER
        ================================================= */

        footer {

            background: #172554;

            color: white;

            padding: 35px 7%;

            display: flex;

            justify-content: space-between;

            align-items: center;

            flex-wrap: wrap;

            gap: 15px;
        }


        footer p {

            color: #cbd5e1;

            font-size: 14px;
        }


        .tech {

            display: flex;

            gap: 12px;
        }


        .tech span {

            background: rgba(255,255,255,0.1);

            padding: 8px 14px;

            border-radius: 20px;

            font-size: 12px;
        }


        /* =================================================
           ANIMATIONS
        ================================================= */

        @keyframes slideLeft {

            from {

                opacity: 0;

                transform: translateX(-40px);
            }

            to {

                opacity: 1;

                transform: translateX(0);
            }
        }


        @keyframes slideRight {

            from {

                opacity: 0;

                transform: translateX(40px);
            }

            to {

                opacity: 1;

                transform: translateX(0);
            }
        }


        /* =================================================
           MOBILE
        ================================================= */

        @media (max-width: 900px) {

            .hero {

                flex-direction: column;

                text-align: center;
            }


            .hero-content {

                width: 100%;
            }


            .hero-image {

                width: 100%;
            }


            .hero p {

                margin-left: auto;

                margin-right: auto;
            }


            .buttons {

                justify-content: center;
            }


            .cards {

                grid-template-columns:
                    repeat(2, 1fr);
            }


            .features {

                grid-template-columns: 1fr;
            }

        }


        @media (max-width: 600px) {

            .nav-links {

                display: none;
            }


            .hero h1 {

                font-size: 38px;
            }


            .cards {

                grid-template-columns: 1fr;
            }


            .hero {

                padding-top: 40px;
            }


            .hero-image {

                height: 300px;
            }

        }

    </style>

</head>


<body>


<!-- =====================================================
     NAVIGATION
===================================================== -->

<nav>

    <div class="logo">

        <div class="logo-icon">
            ♥
        </div>

        Hospital Support

    </div>


    <div class="nav-links">

        <a href="/">
            🏠 Home
        </a>

        <a href="/docs">
            📄 API Docs
        </a>

        <a href="/redoc">
            ℹ About
        </a>

    </div>

</nav>



<!-- =====================================================
     HERO
===================================================== -->

<section class="hero">


    <div class="hero-content">

        <div class="small-title">

            FASTER SUPPORT • BETTER CARE • HEALTHIER TOMORROW

        </div>


        <h1>

            Hospital Support

            <br>

            <span>Request System</span>

        </h1>


        <p>

            A simple and efficient platform to manage
            hospital service requests. Create, track,
            update and manage support requests
            for smooth hospital operations.

        </p>


        <div class="buttons">

            <a
                href="/docs"
                class="primary-btn"
            >

                🚀 View API Documentation

            </a>


            <a
                href="#features"
                class="secondary-btn"
            >

                ✨ Explore System

            </a>

        </div>

    </div>



    <!-- HOSPITAL IMAGE -->

    <div class="hero-image">

        <img
            src="https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=1200&q=85"
            alt="Modern Hospital"
        >


        <div class="image-overlay">

            <h3>
                Modern Hospital Support
            </h3>

            <p>
                Helping hospital teams manage
                service requests efficiently.
            </p>

        </div>

    </div>

</section>



<!-- =====================================================
     CRUD SECTION
===================================================== -->

<section class="section" id="features">


    <div class="section-heading">

        <h2>
            Manage Service Requests
        </h2>

        <p>
            Complete CRUD operations for hospital support requests
        </p>

    </div>



    <div class="cards">


        <!-- CREATE -->

        <div class="card">

            <div class="card-icon green">

                ➕

            </div>


            <h3>
                Create Request
            </h3>


            <p>

                Submit a new service request
                for hospital support.

            </p>


            <a
                href="/docs#/default/create_request_service_requests_post"
                class="card-button green-button"
            >

                Create Now →

            </a>

        </div>



        <!-- READ -->

        <div class="card">

            <div class="card-icon blue">

                🔍

            </div>


            <h3>
                View Requests
            </h3>


            <p>

                View and check all existing
                hospital service requests.

            </p>


            <a
                href="/docs#/default/get_all_requests_service_requests_get"
                class="card-button blue-button"
            >

                View Requests →

            </a>

        </div>



        <!-- UPDATE -->

        <div class="card">

            <div class="card-icon orange">

                ✏️

            </div>


            <h3>
                Update Request
            </h3>


            <p>

                Modify an existing service
                request whenever required.

            </p>


            <a
                href="/docs"
                class="card-button orange-button"
            >

                Update Now →

            </a>

        </div>



        <!-- DELETE -->

        <div class="card">

            <div class="card-icon red">

                🗑️

            </div>


            <h3>
                Delete Request
            </h3>


            <p>

                Remove unwanted service
                requests from the system.

            </p>


            <a
                href="/docs"
                class="card-button red-button"
            >

                Delete Now →

            </a>

        </div>

    </div>

</section>



<!-- =====================================================
     FEATURES
===================================================== -->

<section class="features">


    <div class="feature">

        <div class="feature-icon">
            ❤️
        </div>


        <div>

            <h3>
                Better Patient Support
            </h3>

            <p>
                Manage support requests quickly
                and efficiently.
            </p>

        </div>

    </div>



    <div class="feature">

        <div class="feature-icon">
            🔒
        </div>


        <div>

            <h3>
                Reliable System
            </h3>

            <p>
                FastAPI and MongoDB provide
                reliable backend operations.
            </p>

        </div>

    </div>



    <div class="feature">

        <div class="feature-icon">
            ⚡
        </div>


        <div>

            <h3>
                Fast Operations
            </h3>

            <p>
                Create, read, update and delete
                requests efficiently.
            </p>

        </div>

    </div>

</section>



<!-- =====================================================
     FOOTER
===================================================== -->

<footer>


    <div>

        <strong>
            🏥 Hospital Support Request System
        </strong>

        <p>
            Supporting better hospital operations
        </p>

    </div>


    <div class="tech">

        <span>
            ⚡ FastAPI
        </span>

        <span>
            🍃 MongoDB
        </span>

        <span>
            🐍 Python
        </span>

    </div>


</footer>


</body>

</html>
    """


# =========================================================
# CREATE
# =========================================================

@app.post("/service-requests", status_code=201)
def create_request(payload: ServiceRequest):

    request_data = payload.model_dump()

    result = service_requests.insert_one(request_data)

    new_request = service_requests.find_one(
        {"_id": result.inserted_id}
    )

    return request_helper(new_request)


# =========================================================
# READ ALL
# =========================================================

@app.get("/service-requests")
def get_all_requests():

    docs = service_requests.find()

    return [
        request_helper(doc)
        for doc in docs
    ]


# =========================================================
# READ BY ID
# =========================================================

@app.get("/service-requests/{id}")
def get_request(id: str):

    if not ObjectId.is_valid(id):

        raise HTTPException(
            status_code=400,
            detail="Invalid request ID"
        )

    doc = service_requests.find_one(
        {"_id": ObjectId(id)}
    )

    if not doc:

        raise HTTPException(
            status_code=404,
            detail="Service request not found"
        )

    return request_helper(doc)


# =========================================================
# UPDATE
# =========================================================

@app.put("/service-requests/{id}")
def update_request(
    id: str,
    payload: ServiceRequest
):

    if not ObjectId.is_valid(id):

        raise HTTPException(
            status_code=400,
            detail="Invalid request ID"
        )

    result = service_requests.update_one(

        {"_id": ObjectId(id)},

        {
            "$set": payload.model_dump()
        }

    )

    if result.matched_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Service request not found"
        )

    updated_request = service_requests.find_one(
        {"_id": ObjectId(id)}
    )

    return request_helper(updated_request)


# =========================================================
# DELETE
# =========================================================

@app.delete("/service-requests/{id}")
def delete_request(id: str):

    if not ObjectId.is_valid(id):

        raise HTTPException(
            status_code=400,
            detail="Invalid request ID"
        )

    result = service_requests.delete_one(
        {"_id": ObjectId(id)}
    )

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Service request not found"
        )

    return {
        "message": "Service request deleted successfully"
    }