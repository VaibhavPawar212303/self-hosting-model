# 🧪 Generated Test Cases

**Requirement:** User should be able to log in using email and password.

**Version:** v1

**Mode:** parallel

**Response Time (s):** 399.24

---

## Test Case 1

### Test Case
TC001 - Valid Email and Password Login

### Objective
To verify that user can successfully login using a valid email and password

### Preconditions
- User should have an account on the system
- Email and password combination should be correct

### Test Data
- Valid email (e.g., test@example.com)
- Valid password (e.g., password123)

### Test Steps
- Navigate to login page
- Enter valid email in the 'Email' field
- Enter valid password in the 'Password' field
- Click on the 'Login' button

### Expected Results
- User should be successfully logged in
- User should see dashboard

### Variations
- TC001V1 - Multiple login attempts: Attempt to log in 3 times with same email and password combination

### Edge Cases
- Invalid email format (e.g., abc.def.com)
- Short/weak password (less than 8 characters)

---

## Test Case 2

### Test Case
TC002 - Invalid Email Login

### Objective
To verify that user cannot login using an invalid email and valid password

### Preconditions
- User should have a valid account on the system
- Email combination should be incorrect

### Test Data
- Invalid email (e.g., abcdef)
- Valid password (e.g., password123)

### Test Steps
- Navigate to login page
- Enter invalid email in the 'Email' field
- Enter valid password in the 'Password' field
- Click on the 'Login' button

### Expected Results
- User should not be logged in
- Error message should appear

### Variations
- TC002V1 - Invalid email with correct domain: Attempt to log in using an invalid email with correct domain (e.g., abc@example.com)

### Edge Cases
- Empty email field
- Email field containing only spaces

---

## Test Case 3

### Test Case
TC003 - Invalid Password Login

### Objective
To verify that user cannot login using valid email and invalid password

### Preconditions
- User should have a valid account on the system
- Password combination should be incorrect

### Test Data
- Valid email (e.g., test@example.com)
- Invalid password (e.g., password)

### Test Steps
- Navigate to login page
- Enter valid email in the 'Email' field
- Enter invalid password in the 'Password' field
- Click on the 'Login' button

### Expected Results
- User should not be logged in
- Error message should appear

### Variations
- TC003V1 - Short/weak password: Attempt to log in using a short/weak password (less than 8 characters)

### Edge Cases
- Password field containing only spaces
- Empty password field

---

## Test Case 4

### Test Case
TC_001_LoginWithEmailAndPassword

### Objective
Verify user can log in with correct email and password.

### Preconditions
- User has registered account
- Account is active

### Test Data
- {'email': 'valid_email@gmail.com', 'password': 'correct_password'}

### Test Steps
- Open login page
- Enter email in the input field and select 'Next'
- Enter password in the input field
- Click on 'Login' button

### Expected Results
- User is redirected to dashboard after successful login
- Error message does not appear for correct credentials

---

## Test Case 5

### Test Case
TC_002_LoginWithEmailAndPasswordInvalidCredentials

### Objective
Verify user cannot log in with incorrect email or password.

### Preconditions
- User has registered account

### Test Data
- {'email': 'invalid_email@gmail.com', 'password': 'correct_password'}
- {'email': 'valid_email@gmail.com', 'password': 'incorrect_password'}

### Test Steps
- Open login page
- Enter email in the input field and select 'Next'
- Enter password in the input field
- Click on 'Login' button

### Expected Results
- Error message appears for invalid email or password
- User is not redirected to dashboard after failed login attempt

---

## Test Case 6

### Test Case
TC_003_LoginWithEmailAndPasswordLockedAccount

### Objective
Verify user cannot log in with locked account.

### Preconditions
- User has registered account and account is locked due to multiple failed login attempts

### Test Data
- {'email': 'locked_account@gmail.com', 'password': 'correct_password'}

### Test Steps
- Open login page
- Enter email in the input field and select 'Next'
- Enter password in the input field
- Click on 'Login' button

### Expected Results
- Error message appears for locked account
- User is not redirected to dashboard after failed login attempt

---

## Test Case 7

### Test Case
TC_004_LoginWithEmailAndPasswordForgotPassword

### Objective
Verify user can log in with forgot password flow.

### Preconditions
- User has registered account and does not remember password

### Test Data
- {'email': 'forgot_password@gmail.com'}

### Test Steps
- Open login page
- Click on 'Forgot Password' button
- Enter email in the input field for forgot password flow
- Click on 'Submit' button

### Expected Results
- User receives email with password reset link
- Error message does not appear for correct email

---

## Test Case 8

### Test Case
TC_005_LoginWithEmailAndPasswordMultipleAccounts

### Objective
Verify user can log in with multiple accounts.

### Preconditions
- User has registered multiple accounts

### Test Data
- {'email': 'valid_email1@gmail.com', 'password': 'correct_password'}
- {'email': 'valid_email2@gmail.com', 'password': 'correct_password'}

### Test Steps
- Open login page and select first account
- Enter email in the input field and select 'Next'
- Enter password in the input field
- Click on 'Login' button
- Open login page and select second account
- Enter email in the input field and select 'Next'
- Enter password in the input field
- Click on 'Login' button

### Expected Results
- User is redirected to dashboard after successful login for both accounts
- Error message does not appear for correct credentials

---

