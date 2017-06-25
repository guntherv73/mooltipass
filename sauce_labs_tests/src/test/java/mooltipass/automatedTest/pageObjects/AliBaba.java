package mooltipass.automatedTest.pageObjects;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Action;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
/// Two page login error
public class AliBaba extends AbstractPage{
	
	public AliBaba (WebDriver driver) {
		super(driver);
		PageFactory.initElements(driver, this);
	}


	@FindBy(xpath = "//div[@class='sc-hd-row sc-hd-main']//a[@data-val='ma_signin']")
	private WebElement loginBtn;
	
	@FindBy(xpath = "//input[@id='fm-login-id']")
	private WebElement email;

	@FindBy(id = "fm-login-password")
	private WebElement password;
	
	@FindBy(id = "fm-login-submit")
	private WebElement submitLogin;
	
	@FindBy(xpath = "//a[@data-val='My Alibaba']")
	private WebElement dashBoard;
	
	@FindBy(xpath = " //a[@data-val='ma_signout']")
	private WebElement logoutBtn;
	
	@FindBy(xpath="//input[@type='checkbox']")
	private WebElement rememberMe;

	public void enterEmail(String value){
		driver.switchTo().frame(driver.findElement(By.id("alibaba-login-box" )));
		email.sendKeys(value);
	}

	public void enterPassword(String value){
		
		password.sendKeys(value);
	}
	
	public void goToLogin(){
		waitUntilAppears(loginBtn);
		loginBtn.click();
	}
	
	public void submit(){
	if(rememberMe.isSelected())
		rememberMe.click();
	submitLogin.click();
	}
	public void goTodDashboard()
	{
		waitUntilAppears(dashBoard);
		hover(dashBoard);
		
	}
	public void logout(){
		waitUntilAppears(logoutBtn);
		logoutBtn.click();
		sleep(9000);
	}
	
	public boolean checkLogin(){

		waitUntilAppears(By.xpath("//a[@data-val='My Alibaba']"));
		return isElementPresent(By.xpath("//a[@data-val='My Alibaba']"));
	}
	public boolean checkAtLoginPage(){
		sleep(1000);
		return isElementPresent(By.id("fm-login-id"));
	}
	
	
}
