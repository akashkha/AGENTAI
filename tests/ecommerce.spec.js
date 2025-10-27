const { test, expect } = require('@playwright/test');

test('complete e-commerce purchase flow', async ({ page }) => {
    // Step 1: Login
    await page.goto('https://rahulshettyacademy.com/loginpagePractise/');
    await page.locator('#username').fill('rahulshettyacademy');
    await page.locator('#password').fill('learning');
    await page.locator('#signInBtn').click();
    
    // Wait for products page to load
    await page.waitForURL('**/angularpractice/shop');

    // Step 2: Product Selection
    // Add multiple products to demonstrate a real shopping scenario
    const products = await page.locator('.card-title a');
    const addToCartButtons = page.locator('.card-footer button');
    const productCount = await products.count();
    
    // Add iPhone X and one more product
    for(let i = 0; i < productCount; i++) {
        const productName = await products.nth(i).textContent();
        if(productName.includes('iphone X') || productName.includes('Nokia Edge')) {
            await addToCartButtons.nth(i).click();
        }
    }

    // Step 3: Cart Review
    await page.locator('a.nav-link.btn.btn-primary').click();
    
    // Wait for cart page to load
    await page.waitForSelector('h4.media-heading a');
    
    // Verify products in cart
    const cartItems = await page.locator('h4.media-heading a');
    await expect(cartItems).toContainText(['iphone X', 'Nokia Edge']);

    // Verify cart total
    const totalAmount = await page.locator('h3 strong').textContent();
    expect(totalAmount).toBeTruthy();

    // Step 4: Proceed to Checkout
    await page.waitForSelector('button.btn.btn-success');
    await page.locator('button.btn.btn-success').click();

    // Step 5: Fill Country Details
    await page.waitForSelector('#country');
    await page.locator('#country').type('ind');
    await page.waitForSelector('.suggestions');
    await page.locator('.suggestions a:has-text("India")').click();
    
    // Step 6: Accept Terms and Purchase
    await page.locator('label[for*="checkbox2"]').click();
    await page.locator('input[value="Purchase"]').click();

    // Step 7: Verify Success Message
    await page.waitForSelector('.alert-success');
    const successText = await page.locator('.alert-success').textContent();
    expect(successText).toContain('Success! Thank you!');
    
    console.log('Test passed: Complete purchase flow successful');
});