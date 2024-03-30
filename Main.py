import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def Init():
    global TargetTime, WangZhi, Price, Session, Number, WebDriver

    # 接下来六行需要设置，其余不要动   #建议看到购买成功的提示后，在订单中心确认购买成功后再终止脚本
    TargetTime = "2024-03-29 19:00:00.00000000"  # 设置抢购时间
    WangZhi = "https://show.bilibili.com/platform/detail.html?id=83213&from=pc_ticketlist"  # 设置抢票网址
    Session = '1'  # 场次设置：修改引号内部的数字，数字对应第选项的序号，选项序号从左到右从1开始依次排列
    Price = '2'  # 价格设置：设置方法与场次设置一样
    Number = 2  # 票数设置，注意不要超过限制 #另外，如果是实名制购票的话要先在会员购中心-购买人信息添加好
    chrome_driver_path = 'C:\\Users\\归忆886hyf\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe'  # 指定Chromedriver的路径

    ch_options = Options()
    # ch_options.add_argument("--headless")  # headless表示不打开图形化界面----
    service = Service(chrome_driver_path)  # 创建Service对象
    WebDriver = webdriver.Chrome(service=service, options=ch_options)
    WebDriver.get(WangZhi)  # 输入目标购买页面

    time.sleep(15)
    print("进入购票页面成功")
    print("扫码登录后关闭页面开始抢票")

    # WebDriver.find_element(By.CLASS_NAME, "nav-header-register").click()
    # time.sleep(1)

    # 截取登录二维码并展示    扫完登录后页面不会变化，手动关闭即可
    # WebDriver.save_screenshot('./QRcode.png')-
    # qrimg = cv2.imread('./QRcode.png')-
    # cv2.imshow("qrimg", qrimg)-
    # key = cv2.waitKey(0)-

    # WebDriver.find_element(By.CLASS_NAME, "bili-mini-close").click()

    # 有图形验证码所以不能通过账号密码自动登录
    # USERNAME = '1111111'
    # PASSWORD = '222222'
    # loginName = WebDriver.find_element(By.CLASS_NAME, 'bili-mini-account')
    # loginName.send_keys(USERNAME)
    # loginPwd = WebDriver.find_element(By.CLASS_NAME, 'bili-mini-password')
    # loginPwd.send_keys(PASSWORD)

    # print("请在10s内登录")
    # time.sleep(10)


# def Select():
#     while True:
#         try:
#             WebDriver.find_element(By.XPATH,
#                                    '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[4]/ul[1]/li[2]/div[' + Session + ']').click()
#             WebDriver.find_element(By.XPATH,
#                                    '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[4]/ul[2]/li[2]/div[' + Price + ']').click()
#             # # 定位包含数字的元素
#             # element = WebDriver.find_element_by_class_name("count-number")
#             #
#             # # 修改元素的文本内容为 "2"
#             # WebDriver.execute_script("arguments[0].innerText = '2';", element)
#
#             WebDriver.find_element(By.XPATH,
#                                    '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[4]/ul[3]/li[2]/div/div[3]').click()
#             break
#         except:
#             print("等待刷新")

def Select():
    while True:
        try:
            # 前两个点击只执行一次
            WebDriver.find_element(By.XPATH,
                                   '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[4]/ul[1]/li[2]/div[' + Session + ']').click()
            WebDriver.find_element(By.XPATH,
                                   '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[4]/ul[2]/li[2]/div[' + Price + ']').click()
            # 注意原本数量就是1，因此只需要点击Number-1次
            click_count = 1  # 每次点击后增加计数
            while click_count < Number:
                WebDriver.find_element(By.XPATH,
                                       '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[4]/ul[3]/li[2]/div/div[3]').click()
                click_count += 1
            break  # 执行完点击后跳出循环
        except:
            print("等待刷新")


def Wait():
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("当前时间: " + now + "     抢票时间: " + TargetTime)
        if now >= TargetTime:
            WebDriver.refresh()
            Select()
            break


def Buy():
    print("test1")
    while True:
        try:
            WebDriver.find_element(By.CLASS_NAME, "product-buy.enable").click()
            # time.sleep(5)
            print("进入购买页面成功")
        except:
            print("无法点击购买")

        try:
            if Number == 2:
                # 定位所有符合条件的元素
                elements = WebDriver.find_elements(By.CLASS_NAME, "card-item-container.user-card-item")
                elements[1].click()
            WebDriver.find_element(By.CLASS_NAME, "confirm-paybtn.active").click()
            print("订单创建完成，请在十分钟内付款")
            # 此处不要中断避免被卡出界面造成假报成功
        except:
            print("无法点击创建订单")


if __name__ == '__main__':
    Init()
    Wait()
    Select()
    Buy()
