# Assignment 2
#   Q1 : Explain how you implemented the checklist above step-by-step (not just by following the tutorial).
         : 1. Created a fresh Django project and `main` app (separate from the tutorial repo);
           2. Added `main` to `INSTALLED_APPS`, configured DB/timezone/templates/static in `settings.py`;
           3. Wrote `Product` model with required fields (and my extras), then ran `makemigrations` and `migrate`;
           4. Built `about` view + `about.html` to show app name, my name, and class;
           5. Added project `urls.py` → `include('main.urls')` and mapped routes in `main/urls.py`;
           6. Implemented list/detail pages and a create form;
           7. Implemented XML/JSON endpoints (all and by ID) using `serializers.serialize`;
           8. Tested locally, committed, pushed, and deployed;
           9. Put the public URL and screenshots in `README.md`.

# Q2 : Create a diagram showing the client request to the Django-based web application and its response, and explain the relationship between `urls.py`, `views.py`, `models.py`, and the HTML file in the diagram.
         : Diagram (text): Browser → HTTP request → Project `urls.py` → App `main/urls.py` (pattern match) → `views.py` (logic) → `models.py` (ORM query) → Template (HTML render with context) → HTTP response → Browser;
           `urls.py` routes, `views.py` prepares data/decides response, `models.py` defines and accesses data, the HTML template presents the data.

# Q3 : Explain the role of `settings.py` in a Django project!
         : Central configuration for the whole project: installed apps, middleware, database, static/media, templates, security keys, allowed hosts, i18n/timezone, email/backends, and third-party integrations—so behavior and environment are controlled in one place.

# Q4 : How does database migration work in Django?
         : Django detects model changes and generates migration files with `makemigrations`; applying them with `migrate` runs the necessary SQL to update the schema and records the state in `django_migrations`, enabling incremental, ordered, and often reversible changes.

# Q5 : In your opinion, among all existing frameworks, why is the Django framework chosen as the starting point for learning software development?
         : It’s “batteries-included” (ORM, auth, admin, forms, templates, security), has clear MVT structure and strong conventions, excellent docs, and a mature ecosystem—letting beginners build secure full-stack apps quickly while learning core web concepts without wiring many libraries manually.

# Q6 : Do you have any feedback for the teaching assistant for Tutorial 1 that you previously completed?
         : 

# Assignment 3
# Q1 : Why do we need data delivery (endpoints) in a platform?
         : To let other apps/services (mobile, dashboards, microservices, automation) consume our data reliably via a stable contract (XML/JSON),
           enabling integration, reuse, and decoupling between frontends/backends.

# Q2 : XML vs JSON—why is JSON more popular today?
         : JSON is lighter and less verbose, maps naturally to JS objects, is easy to parse in most languages, and suits REST APIs; XML is powerful
           for document-heavy use (schemas/namespaces) but is typically heavier for web data exchange.

# Q3 : What is the purpose of forms.is_valid() in Django, and why do we need it?
         : is_valid() runs field/clean validation and produces cleaned_data, preventing bad/unsafe input from being saved or used; without it we risk
           incorrect types, missing required fields, injection payloads, and inconsistent database state.

# Q4 : Why do we need {% csrf_token %} when making forms in Django? What if we don’t include it? How can this be exploited?
         : The CSRF token binds a form submission to the user’s session so forged cross-site POSTs are rejected; without it, attackers can trick a
           logged-in user’s browser into submitting malicious state-changing requests (classic Cross-Site Request Forgery).

# Q5 : Explain how you implemented the Assignment 3 checklist step-by-step (not just following the tutorial).
         : 1. Created ProductForm in main/forms.py with my actual fields (name, price, description, thumbnail, category, size, stock, is_featured, for_sale);
           2. Added views: product_list, product_detail, product_create (GET shows form, POST validates/saves, redirects);
           3. Implemented data-delivery views: show_xml, show_json, show_xml_by_id, show_json_by_id using serializers.serialize(...);
           4. Wired URLs in main/urls.py for pages (/, product/add/, product/<id>/) and data (/xml/, /json/, /xml/<id>/, /json/<id>/);
           5. Built templates: product_list.html (links to add/detail/XML/JSON), product_form.html (with {% csrf_token %}), product_detail.html (shows all fields);
           6. Verified GET/POST flow and serialization in the browser and Postman; 7. git add/commit/push and updated README with endpoints and screenshots.

# Q6 : Do you have any feedback for the teaching assistants for Tutorial 2?
         : 

# Assignment 4
# Q1 : What is Django's AuthenticationForm? Explain its advantages and disadvantages.
         : A built-in login form that validates a username/password against Django’s auth backends and exposes     cleaned_data and non-field errors for failed logins.
           Advantages: well-tested, integrates with request (e.g., AuthenticationForm(request, data=...)), good error messages, easy to drop into views/templates, works with CSRF/session middleware.
           Disadvantages: fixed fields (username/password) and default auth flow; customizing UX (email login, extra fields, MFA, rate-limit) requires subclassing or custom forms/views.

# Q2 : What is the difference between authentication and authorization? How does Django implement the two concepts?
         : Authentication answers “who are you?”; authorization answers “what are you allowed to do?”.
           Django authenticates via auth backends + session middleware (populates request.user / request.session); it authorizes via permissions, groups, is_staff/is_superuser, decorators/mixins
           (e.g., @login_required, @permission_required, User.has_perm), and custom object-level checks in views.

# Q3 : What are the benefits and drawbacks of using sessions and cookies in storing the state of a web application?
         : Sessions (server-side): pros—less exposure of data to the client, can store richer state, easy invalidation; cons—server storage/DB hits, scaling/replication concerns.
           Cookies (client-side): pros—simple, stateless server, no DB lookups for tiny flags; cons—size limits (~4KB), sent on every request, client-visible/modifiable, must be signed/secured to prevent tampering.

# Q4 : In web development, is the usage of cookies secure by default, or is there any potential risk that we should be aware of? How does Django handle this problem?
         : Not secure by default—risks include theft via XSS (if not HttpOnly), interception over HTTP (if not Secure), CSRF, and fixation/tampering.
           Django mitigations include HttpOnly/Secure/SameSite cookie settings (SESSION_COOKIE_HTTPONLY, SESSION_COOKIE_SECURE, SESSION_COOKIE_SAMESITE; likewise for CSRF cookies),
           per-request CSRF tokens, signed cookies/session engines, and easy HTTPS enforcement (SECURE_SSL_REDIRECT).

# Q5 : Explain how you implemented the checklist above step-by-step (not just following the tutorial).
         : 1. Added owner = ForeignKey(User, on_delete=CASCADE) to Product and resolved existing rows by assigning a default user id during makemigrations; ran migrate.
           2. Built register/login/logout views using UserCreationForm and AuthenticationForm; login sets a "last_login" cookie, logout deletes it.
           3. Protected pages with @login_required and filtered data per user: product_list shows Product.objects.filter(owner=request.user); product_detail/get uses owner scoping.
           4. On create, set obj = form.save(commit=False); obj.owner = request.user; obj.save(); ensured form fields match the model.
           5. Wired URLs: /register, /login, /logout plus existing list/add/detail and XML/JSON (also scoped to owner).
           6. Made templates: register.html, login.html, and updated product_list header to show {{ user.username }} and {{ last_login }} with a Logout link.
           7. Created two accounts and added three products per account to verify per-user isolation; tested /, /product/add/, /product/<id>/, /xml/, /json/, and by-ID endpoints.
           8. Committed and pushed changes; verified behavior with DEBUG off and confirmed cookies and session flow end-to-end.


# Assignment 5
# Q1 : CSS Selector Priority: If multiple CSS selectors target an HTML element, explain the priority order for CSS selector selection
Order of precedence (highest → lowest):
    1. !important (last resort; avoid if possible)
    2. Inline styles (e.g., <div style="...">)
    3. ID selectors (#id)
    4. Class/attribute/pseudo-class selectors (.class, [type="text"], :hover)
    5. Type (element) and pseudo-element selectors (h1, p, ::before)
    6. The universal selector *, inheritance, and default browser styles

# Q2 : Why is responsive design important in web application development?, Provide examples of applications that have and haven't implemented responsive design, Explain the reasons behind your examples
    Why it Matters: 
    1. Multi-device compatibility: Works on phones, tablets, laptops, desktops.
    2. Usability & accessibility: Legible text, touch-friendly controls, non-overflowing layouts.
    3. Maintainability: One codebase scales across breakpoints.

    Example:
    Has responsive design (example): 
    Football Shop (current) Uses Tailwind utility classes (e.g., max-w-7xl mx-auto px-4, responsive grids), a mobile menu toggle, and fluid layouts—content stacks on small screens and becomes multi-column on larger screens.

    Why this outcome: 
    Tailwind utilities (grid, flex, responsive prefixes like md:, lg:) and sensible container widths make the layout fluid.

# Q3 : Explain the differences between margin, border, and padding, and how to implement them
    Content: The actual text/image/content area.
    Padding: Space inside the border, around content (takes the element’s background color).
    Border: The line surrounding padding + content.
    Margin: Space outside the border, separating the element from neighbors (transparent).
# Implementation : 
    box-sizing: border-box;    
    width: 300px;
    margin: 16px;
    padding: 12px;
    border: 2px solid #e5e7eb;
    background: #fff;

# Q4 : Explain the concepts of flexbox and grid layout along with their uses
    Flexbox (1-D layout):
    Best for rows OR columns (navigation bars, button groups, alignment).
    Axes: main/cross; easy centering and spacing.
    Example: 
    <nav class="flex items-center justify-between gap-4">
        <div>Logo</div>
        <ul class="flex gap-4">
         <li>Home</li><li>Products</li><li>About</li>
        </ul>
    </nav>

    CSS Grid (2-D layout):
    Best for rows AND columns (dashboards, product cards/grids).
    Explicit track sizes and responsive auto-fill patterns.
    Example :
    <ul class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
     <!-- product cards -->
    </ul>

# Q5 : Explain how you implemented the above checklist step-by-step (not just following the tutorial)
    Base layout:
    Created main.html with Tailwind (CDN), {% load static %}, and a consistent container:
    <main class="max-w-7xl mx-auto w-full px-4 py-8">{% block content %}{% endblock %}</main>

    Global styles:
    Added static/global.css and linked it in main.html. Kept form rules under .form-style to avoid conflicts with Tailwind utilities.

    Navbar (responsive):
    Wrote navbar.html using Tailwind classes, added a mobile menu toggle with a small JS snippet, and included it in main.html via {% include "navbar.html" %}.

    Template inheritance:
    Updated login, register, product_list, product_detail, and product_form to {% extends "main.html" %} and replaced inline styles with Tailwind utilities.

    Responsive components:

    Product list uses Grid (grid-cols-1 sm:grid-cols-2 lg:grid-cols-3) for cards.
    Detail view uses a responsive two-column layout on larger screens and stacks on small screens.
    Buttons/links use consistent Tailwind classes for hover/focus states.

    Forms:
    Wrapped Django forms in a <form class="form-style ..."> so global.css enhances the inputs (padding, borders, focus rings) while Tailwind handles spacing/layout.

    Testing at breakpoints:
    Tested mobile (≤375px), tablet (~768px), and desktop (≥1024px) in browser dev tools to confirm no overflow, readable text, and accessible touch targets.

