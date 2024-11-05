# Multilingual Flask Application

This project demonstrates how to create a multilingual Flask web application by:

- Parametrizing Flask templates to display content in multiple languages.
- Inferring locale based on URL parameters, user settings, or request headers.
- Localizing timestamps to ensure dates and times are displayed according to the user's locale.

### Features
## 1. Parametrized Templates for Multiple Languages

The app dynamically displays content in different languages based on the user's preferences. By parameterizing templates, the application can handle multiple languages and serve localized content to users seamlessly.
## 2. Locale Inference

The application infers the user’s locale by checking:

    URL parameters: Users can pass a language code as part of the URL, like /en/home for English or /fr/home for French.
    User settings: For authenticated users, their preferred language is saved in their profile and retrieved during each session.
    Request headers: For guests, the Accept-Language header in the request provides a default locale based on their browser’s settings.

## 3. Timestamp Localization

To enhance the user experience, timestamps are localized to match the inferred or chosen locale. This includes converting date formats and times to reflect the user's regional preferences.
#### Getting Started
### Prerequisites

-Python 3.7+
-Flask and Babel for managing translations and locale configurations
-Jinja2 for templating

#### Installation

##### Clone the repository:

```bash

git clone https://github.com/Termication/alx-backend.git
cd 0x02-i18n
```
##### Set up the environment:

```bash

python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```
##### Install dependencies:

```bash

pip install -r requirements.txt
```
##### Configure translation files:

Use pybabel to initialize and compile translations in desired languages.
    Example:

```bash

pybabel init -i messages.pot -d translations -l fr  # Initialize French translations
pybabel compile -d translations                     # Compile translations
```
##### Run the application:

```bash

flask run
```
#### Usage
### URL Parameter-Based Language Switching

To display the app in a different language, add a language code to the URL:

    Example: /en/home for English, /es/home for Spanish.

### User Profile Language Settings

For logged-in users, set their preferred language in their profile settings. This language preference will be used throughout the application during their session.
### Localized Date and Time

All timestamps are automatically localized to the user’s preferred language and regional settings. This ensures a consistent experience for users across different time zones and languages.
### Additional Information
### Customizing Language Support

#### To add support for a new language:

Create translation files:

```bash

pybabel init -i messages.pot -d translations -l <new_language_code>
```
Translate the entries in the newly created .po file under the translations directory.
##### Compile translations:

```bash

pybabel compile -d translations
```
