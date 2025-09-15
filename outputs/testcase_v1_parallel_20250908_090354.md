# 🧪 Generated Test Cases

**Requirement:** User should be able to log in using email and password.

**Version:** v1

**Mode:** parallel

**Response Time (s):** 468.86

---

## Test Case 1

### Test Case
TC_001_LoginWithEmailPassword

### Objective
Verify user can login with email and password

### Preconditions
- User must have a registered account
- Application is fully functional

### Test Data
- ValidEmail1@example.com, Password123!
- ValidEmail2@example.com, Password456!

### Test Steps
- Open the application and navigate to login page
- Enter email and password in respective fields
- Click on login button
- Verify user is logged in successfully

### Expected Results
- User is logged in successfully
- Error message for invalid credentials

### Variations
- TC_002_LoginWithEmailPassword_V1: Use email with special characters

---

## Test Case 2

### Test Case
TC_002_LoginWithEmailPassword_V1

### Objective
Verify user can login with email containing special characters

### Preconditions
- User must have a registered account
- Application is fully functional

### Test Data
- SpecialCharEmail@example.com, Password123!
- InvalidCharEmail!@example.com, Password456!

### Test Steps
- Open the application and navigate to login page
- Enter email and password in respective fields
- Click on login button
- Verify user is logged in successfully

### Expected Results
- User is logged in successfully
- Error message for invalid characters

### Variations

### Edge Cases
- TC_003_LoginWithEmailPassword_Edge: Test with empty password

---

## Test Case 3

### Test Case
TC_003_LoginWithEmailPassword_Edge

### Objective
Verify user cannot login with empty password

### Preconditions
- User must have a registered account
- Application is fully functional

### Test Data
- ValidEmail1@example.com, 
- InvalidEmail2!@example.com, Password123!

### Test Steps
- Open the application and navigate to login page
- Enter email and password in respective fields
- Click on login button
- Verify error message for empty password

### Expected Results
- Error message for empty password
- User is logged out

### Variations

### Edge Cases

---

## Test Case 4

### Test Case
TC001_Login_With_Valid_Email_Password

### Objective
Verify user can log in using a valid email and password

### Preconditions
- User account is created with valid email and password

### Test Data
- {'email': 'valid_email@example.com', 'password': 'correct_password'}
- {'email': 'another_valid_email@example.com', 'password': 'another_correct_password'}

### Test Steps
- Open the login page
- Enter a valid email in the email field
- Enter a correct password in the password field
- Click on the Login button

### Expected Results
- User is redirected to the dashboard page
- User name appears next to the profile picture

### Variations

### Edge Cases
- Test with invalid email, test with empty password

---

## Test Case 5

### Test Case
TC002_Login_With_Invalid_Email_Password

### Objective
Verify user cannot log in using an invalid email and password

### Preconditions
- User account is created with valid email and password

### Test Data
- {'email': 'invalid_email', 'password': 'wrong_password'}
- {'email': 'another_invalid_email', 'password': ''}

### Test Steps
- Open the login page
- Enter an invalid email in the email field
- Enter a wrong password in the password field
- Click on the Login button

### Expected Results
- Error message appears saying 'Invalid Email'
- Error message appears saying 'Incorrect Password'

### Variations

### Edge Cases
- Test with valid email and invalid password, test with empty email

---

## Test Case 6

### Test Case
TC003_Login_With_Expired_Session

### Objective
Verify user cannot log in when session is expired

### Preconditions
- User account is created with valid email and password

### Test Data
- {'email': 'valid_email@example.com', 'password': 'correct_password'}

### Test Steps
- Open the login page
- Enter a valid email in the email field
- Leave the session inactive for some time
- Try to log in again

### Expected Results
- Error message appears saying 'Session Expired'

### Variations

### Edge Cases

---

## Test Case 7

### Test Case
TC004_Login_With_Blocking_IP

### Objective
Verify user cannot log in when IP is blocked

### Preconditions
- User account is created with valid email and password

### Test Data
- {'email': 'valid_email@example.com', 'password': 'correct_password'}

### Test Steps
- Open the login page from a blocked IP address
- Enter a valid email in the email field
- Enter a correct password in the password field
- Click on the Login button

### Expected Results
- Error message appears saying 'Your IP is Blocked'

### Variations

### Edge Cases

---

## Test Case 8

### Test Case
TC005_Login_With_Temporarily_Disabled_Account

### Objective
Verify user cannot log in when account is temporarily disabled

### Preconditions
- User account is created with valid email and password

### Test Data
- {'email': 'valid_email@example.com', 'password': 'correct_password'}

### Test Steps
- Open the login page
- Enter a valid email in the email field
- Enter a correct password in the password field
- Click on the Login button

### Expected Results
- Error message appears saying 'Your Account is Temporarily Disabled'

### Variations

### Edge Cases

---

