# Assignment 2
#   Q1 : Explain how you implemented the checklist above step-by-step (not just by following the tutorial).
#         : 1. Created a fresh Django project and `main` app (separate from the tutorial repo);
#           2. Added `main` to `INSTALLED_APPS`, configured DB/timezone/templates/static in `settings.py`;
#           3. Wrote `Product` model with required fields (and my extras), then ran `makemigrations` and `migrate`;
#           4. Built `about` view + `about.html` to show app name, my name, and class;
#           5. Added project `urls.py` → `include('main.urls')` and mapped routes in `main/urls.py`;
#           6. Implemented list/detail pages and a create form;
#           7. Implemented XML/JSON endpoints (all and by ID) using `serializers.serialize`;
#           8. Tested locally, committed, pushed, and deployed;
#           9. Put the public URL and screenshots in `README.md`.

# Q2 : Create a diagram showing the client request to the Django-based web application and its response, and explain the relationship between `urls.py`, `views.py`, `models.py`, and the HTML file in the diagram.
#         : Diagram (text): Browser → HTTP request → Project `urls.py` → App `main/urls.py` (pattern match) → `views.py` (logic) → `models.py` (ORM query) → Template (HTML render with context) → HTTP response → Browser;
#           `urls.py` routes, `views.py` prepares data/decides response, `models.py` defines and accesses data, the HTML template presents the data.

# Q3 : Explain the role of `settings.py` in a Django project!
#         : Central configuration for the whole project: installed apps, middleware, database, static/media, templates, security keys, allowed hosts, i18n/timezone, email/backends, and third-party integrations—so behavior and environment are controlled in one place.

# Q4 : How does database migration work in Django?
#         : Django detects model changes and generates migration files with `makemigrations`; applying them with `migrate` runs the necessary SQL to update the schema and records the state in `django_migrations`, enabling incremental, ordered, and often reversible changes.

# Q5 : In your opinion, among all existing frameworks, why is the Django framework chosen as the starting point for learning software development?
#         : It’s “batteries-included” (ORM, auth, admin, forms, templates, security), has clear MVT structure and strong conventions, excellent docs, and a mature ecosystem—letting beginners build secure full-stack apps quickly while learning core web concepts without wiring many libraries manually.

# Q6 : Do you have any feedback for the teaching assistant for Tutorial 1 that you previously completed?
#         : Great pacing and demos; suggestions: add a quick pitfalls slide (`urls.py` patterns, `INSTALLED_APPS` misses), show one mini deploy end-to-end, and provide a final checklist (repo structure, one view + template works, runserver OK) for self-verification.

# Assignment 3
# Q1 : Why do we need data delivery (endpoints) in a platform?
#         : To let other apps/services (mobile, dashboards, microservices, automation) consume our data reliably via a stable contract (XML/JSON),
#           enabling integration, reuse, and decoupling between frontends/backends.

# Q2 : XML vs JSON—why is JSON more popular today?
#         : JSON is lighter and less verbose, maps naturally to JS objects, is easy to parse in most languages, and suits REST APIs; XML is powerful
#           for document-heavy use (schemas/namespaces) but is typically heavier for web data exchange.

# Q3 : What is the purpose of forms.is_valid() in Django, and why do we need it?
#         : is_valid() runs field/clean validation and produces cleaned_data, preventing bad/unsafe input from being saved or used; without it we risk
#           incorrect types, missing required fields, injection payloads, and inconsistent database state.

# Q4 : Why do we need {% csrf_token %} when making forms in Django? What if we don’t include it? How can this be exploited?
#         : The CSRF token binds a form submission to the user’s session so forged cross-site POSTs are rejected; without it, attackers can trick a
#           logged-in user’s browser into submitting malicious state-changing requests (classic Cross-Site Request Forgery).

# Q5 : Explain how you implemented the Assignment 3 checklist step-by-step (not just following the tutorial).
#         : 1. Created ProductForm in main/forms.py with my actual fields (name, price, description, thumbnail, category, size, stock, is_featured, for_sale);
#           2. Added views: product_list, product_detail, product_create (GET shows form, POST validates/saves, redirects);
#           3. Implemented data-delivery views: show_xml, show_json, show_xml_by_id, show_json_by_id using serializers.serialize(...);
#           4. Wired URLs in main/urls.py for pages (/, product/add/, product/<id>/) and data (/xml/, /json/, /xml/<id>/, /json/<id>/);
#           5. Built templates: product_list.html (links to add/detail/XML/JSON), product_form.html (with {% csrf_token %}), product_detail.html (shows all fields);
#           6. Verified GET/POST flow and serialization in the browser and Postman; 7. git add/commit/push and updated README with endpoints and screenshots.

# Q6 : Do you have any feedback for the teaching assistants for Tutorial 2?
#         : Clear and helpful—one suggestion: include a short “common errors” slide (serialize vs seralize typo, missing {% csrf_token %}, filter vs get for serializers)
#           and a tiny Postman demo so everyone captures the four endpoint screenshots correctly.
