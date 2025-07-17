# FreightForge Object Repository

This object repository is designed for Selenium WebDriver automation of the FreightForge Streamlit application.

| Element Name | Type | Page/Section | Locator Strategy |
|--------------|------|---------------|------------------|
| Welcome Title | Header | Welcome | xpath=//h1[contains(text(),'FreightForge')] |
| Demo Instructions | Subheader | Welcome | xpath=//h2[contains(text(),'Demo Instructions')] |
| Sidebar Menu | Radio | Sidebar | xpath=//div[@role='radiogroup'] |
| Menu Option - Register & Login | Radio Option | Sidebar | xpath=//label[contains(text(),'Register & Login')] |
| Menu Option - Freight Inquiry & Booking | Radio Option | Sidebar | xpath=//label[contains(text(),'Freight Inquiry & Booking')] |
| Menu Option - Track Shipment | Radio Option | Sidebar | xpath=//label[contains(text(),'Track Shipment')] |
| Tab - Register | Tab | Register & Login | xpath=//button[contains(text(),'Register')] |
| Business Name | Input | Register | xpath=//input[@aria-label='Business Name'] |
| Contact Person | Input | Register | xpath=//input[@aria-label='Contact Person'] |
| Email | Input | Register | xpath=//input[@aria-label='Email'] |
| Mobile Number | Input | Register | xpath=//input[@aria-label='Mobile Number'] |
| PAN/GST Number | Input | Register | xpath=//input[@aria-label='PAN/GST Number'] |
| Business Type | Select | Register | xpath=//div[@role='combobox'] |
| Business Address | Textarea | Register | xpath=//textarea[@aria-label='Business Address'] |
| Desired Username | Input | Register | xpath=//input[@aria-label='Desired Username'] |
| Password | Password | Register | xpath=//input[@type='password'] |
| Upload Document | FileUploader | Register | xpath=//input[@type='file'] |
| Send OTP Button | Button | Register | xpath=//button[contains(text(),'Send OTP')] |
| OTP Input | Input | Register | xpath=//input[@aria-label='Enter OTP'] |
| Verify OTP Button | Button | Register | xpath=//button[contains(text(),'Verify OTP')] |
| Tab - Login | Tab | Register & Login | xpath=//button[contains(text(),'Login')] |
| Login Username | Input | Login | xpath=//input[@aria-label='Username'] |
| Login Password | Password | Login | xpath=//input[@type='password'] |
| Login Button | Button | Login | xpath=//button[contains(text(),'Login')] |
| Tab - Admin Approvals | Tab | Register & Login | xpath=//button[contains(text(),'Admin Approvals')] |
| Approve Button | Button | Admin Approvals | xpath=//button[contains(text(),'Approve')] |
| Reject Button | Button | Admin Approvals | xpath=//button[contains(text(),'Reject')] |
| Goods Type | Select | Freight Inquiry & Booking | xpath=//div[@role='combobox'] |
| Quantity | NumberInput | Freight Inquiry & Booking | xpath=//input[@type='number'] |
| Origin | Input | Freight Inquiry & Booking | xpath=//input[@aria-label='Origin'] |
| Destination | Input | Freight Inquiry & Booking | xpath=//input[@aria-label='Destination'] |
| Dispatch Date | DateInput | Freight Inquiry & Booking | xpath=//input[@type='date'] |
| Check Rates Button | Button | Freight Inquiry & Booking | xpath=//button[contains(text(),'Check Rates')] |
| Wagon Option | Radio | Freight Inquiry & Booking | xpath=//div[@role='radiogroup'] |
| Book & Pay Button | Button | Freight Inquiry & Booking | xpath=//button[contains(text(),'Book & Pay Now')] |
| Waybill Reference Input | Input | Track Shipment | xpath=//input[@aria-label='Enter Waybill Reference'] |
| Track Now Button | Button | Track Shipment | xpath=//button[contains(text(),'Track Now')] |
| Simulate Delivery Button | Button | Track Shipment | xpath=//button[contains(text(),'Simulate Delivery')] |
| Download Waybill Button | DownloadButton | Freight Inquiry & Booking | xpath=//button[contains(text(),'Download PDF Waybill')] |
