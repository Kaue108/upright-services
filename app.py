from flask import Flask, request, render_template_string
import csv
import os
from datetime import datetime


app = Flask(__name__)

CSV_FILE = "leads.csv" 

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cleaning, Construction & General Services | Your Home, Our Care</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        :root {
            --bg: #f3f4f6;
            --bg-alt: #ffffff;
            --card: #ffffff;
            --accent-red: #d62828;
            --accent-blue: #003566;
            --accent: var(--accent-red);
            --accent-soft: rgba(214, 40, 40, 0.08);
            --text: #111827;
            --text-soft: #4b5563;
            --border: #e5e7eb;
            --radius: 16px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: radial-gradient(circle at top, #e5e7eb, #ffffff);
            color: var(--text);
            line-height: 1.6;
        }

        a {
            color: inherit;
            text-decoration: none;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 1.25rem;
        }

        /* HEADER */
        .header {
            position: sticky;
            top: 0;
            z-index: 50;
            backdrop-filter: blur(10px);
            background: rgba(255,255,255,0.9);
            border-bottom: 1px solid var(--border);
            box-shadow: 0 4px 12px rgba(15,23,42,0.04);
        }

        .nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.7rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.55rem;
        }

        .logo-img {
            width: 40px;
            height: 40px;
            object-fit: contain;
        }

        .logo-text {
            font-weight: 700;
            font-size: 1rem;
            letter-spacing: 0.04em;
            color: var(--accent-blue);
        }

        .nav-links {
            display: flex;
            gap: 1.2rem;
            font-size: 0.9rem;
            color: var(--text-soft);
        }

        .nav-links a {
            position: relative;
            padding-bottom: 2px;
        }

        .nav-links a::after {
            content: "";
            position: absolute;
            left: 0;
            bottom: 0;
            width: 0;
            height: 2px;
            background: var(--accent);
            transition: width 0.18s ease-out;
        }

        .nav-links a:hover::after {
            width: 100%;
        }

        /* BUTTONS */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            padding: 0.45rem 1.2rem;
            font-size: 0.9rem;
            border: 1px solid var(--accent-blue);
            background: transparent;
            color: var(--accent-blue);
            cursor: pointer;
            transition: all 0.18s ease-out;
            gap: 0.35rem;
            white-space: nowrap;
        }

        .btn-primary {
            background: linear-gradient(to right, var(--accent-red), #f25454);
            border-color: transparent;
            color: #ffffff;
            font-weight: 600;
            box-shadow: 0 10px 22px rgba(214,40,40,0.35);
        }

        .btn-primary:hover {
            transform: translateY(-1px) scale(1.01);
            box-shadow: 0 12px 28px rgba(214,40,40,0.45);
        }

        .btn-outline {
            background: #ffffff;
        }

        .btn-outline:hover {
            background: #f9fafb;
        }

        .btn-ghost {
            border-color: transparent;
            color: var(--text-soft);
        }

        .btn-ghost:hover {
            border-color: var(--border);
            background: #f9fafb;
        }

        /* HERO */
        .hero {
            padding: 3rem 0 2.4rem;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: minmax(0, 3fr) minmax(0, 2.5fr);
            gap: 2.3rem;
            align-items: center;
        }

        .hero-kicker {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.18em;
            color: var(--accent-blue);
            font-weight: 600;
            margin-bottom: 0.7rem;
        }

        .hero h1 {
            font-size: clamp(2rem, 3vw, 2.4rem);
            line-height: 1.2;
            margin-bottom: 0.8rem;
            color: #0f172a;
        }

        .hero-subtitle {
            color: var(--text-soft);
            font-size: 0.98rem;
            max-width: 32rem;
        }

        .hero-ctas {
            margin-top: 1.4rem;
            display: flex;
            gap: 0.8rem;
            flex-wrap: wrap;
        }

        .hero-badges {
            margin-top: 1.6rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.9rem;
            font-size: 0.78rem;
        }

        .hero-badges > div {
            padding: 0.5rem 0.8rem;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: #ffffff;
            box-shadow: 0 4px 8px rgba(148,163,184,0.2);
        }

        .hero-badges strong {
            display: block;
            font-size: 0.82rem;
            color: var(--accent-blue);
        }

        .hero-badges span {
            color: var(--text-soft);
        }

        .hero-card {
            border-radius: 20px;
            padding: 1.4rem 1.5rem;
            border: 1px solid var(--border);
            background: #ffffff;
            box-shadow: 0 18px 40px rgba(15,23,42,0.08);
        }

        .hero-card h2 {
            font-size: 1.15rem;
            margin-bottom: 0.4rem;
            color: #111827;
        }

        .hero-card p {
            font-size: 0.9rem;
            color: var(--text-soft);
            margin-bottom: 0.8rem;
        }

        .hero-list {
            list-style: none;
            font-size: 0.86rem;
            color: var(--text-soft);
            display: grid;
            gap: 0.3rem;
            margin-bottom: 1.1rem;
        }

        /* SECTIONS */
        .section {
            padding: 2.2rem 0;
        }

        .section-title {
            font-size: 1.4rem;
            margin-bottom: 0.3rem;
            color: #111827;
        }

        .section-subtitle {
            color: var(--text-soft);
            font-size: 0.9rem;
            max-width: 32rem;
        }

        /* GRID */
        .grid-3 {
            margin-top: 1.6rem;
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1.1rem;
        }

        .card {
            border-radius: var(--radius);
            border: 1px solid var(--border);
            background: var(--card);
            padding: 1rem 1.1rem;
            font-size: 0.9rem;
            box-shadow: 0 10px 24px rgba(148,163,184,0.18);
        }

        .card h3 {
            font-size: 1rem;
            margin-bottom: 0.4rem;
            color: var(--accent-blue);
        }

        .card p {
            color: var(--text-soft);
            font-size: 0.86rem;
            margin-bottom: 0.6rem;
        }

        .card-list {
            list-style: none;
            font-size: 0.8rem;
            color: var(--text-soft);
            display: grid;
            gap: 0.18rem;
        }

        /* ABOUT + REVIEWS */
        .about-grid {
            display: grid;
            grid-template-columns: minmax(0, 3fr) minmax(0, 2.4fr);
            gap: 1.6rem;
            margin-top: 1.4rem;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            font-size: 0.78rem;
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: #ffffff;
            color: var(--accent-blue);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
        }

        .reviews {
            display: grid;
            gap: 0.7rem;
        }

        .review {
            font-size: 0.8rem;
            border-radius: 12px;
            padding: 0.7rem 0.8rem;
            border: 1px solid var(--border);
            background: #ffffff;
            box-shadow: 0 6px 18px rgba(148,163,184,0.22);
        }

        .stars {
            color: #f59e0b;
            font-size: 0.8rem;
            margin-bottom: 0.2rem;
        }

        .review-name {
            margin-top: 0.3rem;
            font-size: 0.78rem;
            color: var(--text-soft);
        }

        /* CONTACT */
        .contact-grid {
            display: grid;
            grid-template-columns: minmax(0, 3fr) minmax(0, 2fr);
            gap: 1.6rem;
            margin-top: 1.4rem;
        }

        form {
            display: grid;
            gap: 0.85rem;
        }

        .field {
            display: grid;
            gap: 0.25rem;
        }

        label {
            font-size: 0.82rem;
            color: var(--text-soft);
        }

        input, select, textarea {
            background: #ffffff;
            border-radius: 10px;
            border: 1px solid var(--border);
            padding: 0.55rem 0.65rem;
            color: var(--text);
            font-size: 0.9rem;
            outline: none;
            transition: border 0.16s ease-out, box-shadow 0.16s ease-out;
        }

        input:focus, select:focus, textarea:focus {
            border-color: var(--accent-red);
            box-shadow: 0 0 0 1px rgba(214,40,40,0.25);
        }

        textarea {
            min-height: 90px;
            resize: vertical;
        }

        .contact-info {
            font-size: 0.86rem;
            color: var(--text-soft);
            display: grid;
            gap: 0.7rem;
        }

        .contact-box {
            border-radius: var(--radius);
            border: 1px dashed var(--border);
            padding: 0.9rem 0.9rem;
            background: #ffffff;
        }

        .contact-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.18em;
            color: var(--text-soft);
        }

        .contact-value {
            margin-top: 0.25rem;
            font-size: 0.9rem;
            color: var(--text);
        }

        .small {
            font-size: 0.78rem;
            color: var(--text-soft);
        }

        .alert-success {
            border-radius: 999px;
            padding: 0.6rem 0.9rem;
            background: var(--accent-soft);
            border: 1px solid rgba(214,40,40,0.5);
            color: #7f1d1d;
            font-size: 0.8rem;
            margin-bottom: 0.9rem;
        }

        /* FOOTER */
        .footer {
            border-top: 1px solid var(--border);
            padding: 1.2rem 0 2rem;
            margin-top: 1.6rem;
            font-size: 0.8rem;
            color: var(--text-soft);
            background: #ffffff;
        }

        .footer-row {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.8rem;
        }

        /* RESPONSIVE */
        @media (max-width: 900px) {
            .hero-grid,
            .about-grid,
            .contact-grid,
            .grid-3 {
                grid-template-columns: 1fr;
            }

            .hero {
                padding-top: 2.2rem;
            }

            .nav-links {
                display: none;
            }

            .hero-card {
                order: -1;
            }
        }
    </style>
</head>
<body>
<header class="header">
    <div class="container nav">
        <div class="logo">
            <img src="{{ url_for('static', filename='logo.jpeg') }}" alt="Company logo" class="logo-img">
            <span class="logo-text">Cleaning • Construction • Repairs</span>
        </div>
        <nav class="nav-links">
            <a href="#services">Services</a>
            <a href="#about">About</a>
            <a href="#reviews">Reviews</a>
            <a href="#contact">Contact</a>
        </nav>
        <a href="#contact" class="btn btn-outline">Free Quote</a>
    </div>
</header>

<main>
    <!-- HERO -->
    <section class="hero">
        <div class="container hero-grid">
            <div>
                <div class="hero-kicker">Cleaning • Construction • General repairs</div>
                <h1>From cleaning to construction, we take care of your home.</h1>
                <p class="hero-subtitle">
                    Professional house cleaning, small construction projects and general repairs.
                    Serving homeowners and landlords with reliable, high-quality work.
                </p>
                <div class="hero-ctas">
                    <a href="#contact" class="btn btn-primary">
                        Get a free estimate →
                    </a>
                    <a href="#services" class="btn btn-ghost">
                        View all services
                    </a>
                </div>
                <div class="hero-badges">
                    <div>
                        <strong>50+ happy clients</strong>
                        <span>homes cleaned & repaired</span>
                    </div>
                    <div>
                        <strong>5★ rated</strong>
                        <span>for quality & trust</span>
                    </div>
                    <div>
                        <strong>Fast response</strong>
                        <span>same-day contact</span>
                    </div>
                </div>
            </div>
            <div class="hero-card">
                <h2>Need help with your home?</h2>
                <p>We handle cleaning, construction and repairs so you don’t have to.</p>
                <ul class="hero-list">
                    <li>✔ House & apartment cleaning</li>
                    <li>✔ Small construction & remodeling</li>
                    <li>✔ General repairs & maintenance</li>
                </ul>
                <p class="small">Scroll down and send us a message. We will reply as soon as possible.</p>
            </div>
        </div>
    </section>

    <!-- SERVICES -->
    <section id="services" class="section">
        <div class="container">
            <h2 class="section-title">Our Services</h2>
            <p class="section-subtitle">
                Complete solutions for your house – from deep cleaning to small construction and general repairs.
            </p>
            <div class="grid-3">
                <div class="card">
                    <h3>House Cleaning</h3>
                    <p>
                        Regular, deep and move-in/move-out cleaning. We take care of every detail so your home feels fresh and organized.
                    </p>
                    <ul class="card-list">
                        <li>One-time or recurring cleaning</li>
                        <li>Move-in / move-out cleaning</li>
                        <li>Airbnb & rental cleaning</li>
                    </ul>
                </div>
                <div class="card">
                    <h3>Construction & Remodeling</h3>
                    <p>
                        Small construction projects to update and improve your space with quality and safety.
                    </p>
                    <ul class="card-list">
                        <li>Drywall, painting & finishing</li>
                        <li>Flooring and small remodeling</li>
                        <li>Porches, fences and more</li>
                    </ul>
                </div>
                <div class="card">
                    <h3>General Repairs</h3>
                    <p>
                        Day-to-day fixes to keep your house in perfect condition, inside and outside.
                    </p>
                    <ul class="card-list">
                        <li>Minor plumbing & electrical</li>
                        <li>Door, trim & cabinet repairs</li>
                        <li>Handyman & maintenance services</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- ABOUT + REVIEWS -->
    <section id="about" class="section">
        <div class="container about-grid">
            <div>
                <span class="pill">About us</span>
                <h2 class="section-title">Family-owned, detail-focused and committed to your home.</h2>
                <p class="section-subtitle">
                    We are a small business focused on house cleaning, construction and general services.
                    Our goal is simple: to deliver honest work, clear communication and results you can see.
                </p>
                <p class="section-subtitle" style="margin-top: 0.6rem;">
                    We know how important your home is. That’s why we work with respect, punctuality and
                    attention to every detail – as if it were our own.
                </p>
            </div>
            <div id="reviews">
                <h3 style="font-size: 1rem; margin-bottom: 0.5rem;">What our clients say</h3>
                <div class="reviews">
                    <div class="review">
                        <div class="stars">★★★★★</div>
                        “They cleaned and repaired our house before we moved in. Everything looked brand new.
                        Great communication and very professional.”
                        <div class="review-name">— Sarah M.</div>
                    </div>
                    <div class="review">
                        <div class="stars">★★★★★</div>
                        “Excellent job with the painting and small construction we needed in the backyard.
                        I highly recommend their services.”
                        <div class="review-name">— John D.</div>
                    </div>
                    <div class="review">
                        <div class="stars">★★★★★</div>
                        “Fast response, fair price and great quality. They now do our regular cleaning every month.”
                        <div class="review-name">— Amanda R.</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- CONTACT -->
    <section id="contact" class="section">
        <div class="container">
            <h2 class="section-title">Request your free estimate</h2>
            <p class="section-subtitle">
                Tell us what you need and we will contact you to schedule a visit or send an estimate.
            </p>

            <div class="contact-grid">
                <div>
                    {% if message_sent %}
                    <div class="alert-success">
                        Thank you! Your message has been sent. We will contact you as soon as possible.
                    </div>
                    {% endif %}

                    <form method="POST" action="#contact">
                        <div class="field">
                            <label for="name">Name *</label>
                            <input id="name" name="name" type="text" placeholder="Your full name" required>
                        </div>
                        <div class="field">
                            <label for="email">Email *</label>
                            <input id="email" name="email" type="email" placeholder="you@example.com" required>
                        </div>
                        <div class="field">
                            <label for="phone">Phone / WhatsApp *</label>
                            <input id="phone" name="phone" type="tel" placeholder="+1 (555) 000-0000" required>
                        </div>
                        <div class="field">
                            <label for="service_type">What do you need? *</label>
                            <select id="service_type" name="service_type" required>
                                <option value="">Select an option</option>
                                <option value="House cleaning">House cleaning</option>
                                <option value="Construction / remodeling">Construction / remodeling</option>
                                <option value="General repairs">General repairs</option>
                                <option value="Multiple services">Multiple services</option>
                            </select>
                        </div>
                        <div class="field">
                            <label for="message">Describe your project</label>
                            <textarea id="message" name="message" placeholder="Tell us briefly what you need: type of service, number of rooms, dates, etc."></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">
                            Send message
                        </button>
                        <p class="small">We respect your time and privacy. We only use your contact info to reply to your request.</p>
                    </form>
                </div>
                <div class="contact-info">
                    <div class="contact-box">
                        <div class="contact-label">Contact</div>
                        <div class="contact-value">
                            Phone / WhatsApp: <strong>(xxx) xxx-xxxx</strong><br>
                            Email: <strong>youremail@example.com</strong>
                        </div>
                    </div>
                    <div class="contact-box">
                        <div class="contact-label">Service area</div>
                        <div class="contact-value">
                            We serve clients in <strong>your city / region</strong> and nearby areas.
                        </div>
                    </div>
                    <p class="small">
                        Prefer to send a message? Click the button below and contact us directly.
                    </p>
                    <a href="#contact" class="btn btn-outline" style="max-width: 210px;">
                        Message us now
                    </a>
                </div>
            </div>
        </div>
    </section>
</main>

<footer class="footer">
    <div class="container footer-row">
        <span>© {{ year }} Cleaning • Construction • Repairs. All rights reserved.</span>
        <span>Licensed • Insured • Professional home services</span>
    </div>
</footer>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    message_sent = False

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        service_type = request.form.get("service_type")
        message = request.form.get("message")

        print("=== NEW LEAD ===")
        print("Name:", name)
        print("Email:", email)
        print("Phone:", phone)
        print("Service:", service_type)
        print("Message:", message)
        print("================")

        # ---- salvar no CSV ----
        file_exists = os.path.isfile(CSV_FILE)

        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Se o arquivo é novo, escreve o cabeçalho
            if not file_exists:
                writer.writerow(["name", "email", "phone", "service_type", "message", "created_at"])

            writer.writerow([
                name,
                email,
                phone,
                service_type,
                message,
                datetime.now().isoformat()   # 👈 usa o datetime importado lá em cima
            ])
        # ---- fim salvar no CSV ----

        message_sent = True

    year = datetime.now().year   # 👈 também usa o mesmo datetime
    return render_template_string(HTML, message_sent=message_sent, year=year)



if __name__ == "__main__":
    app.run(debug=True)
