## CDN

#### 添加域名

1. 进入网址https://cdn.console.aliyun.com/overview

2. 选择**域名管理**->**添加域名**

3. 这里是填写添加域名的信息：
   1. **加速域名**空可以填*.test.com类型的域名，代表所有test.com一级域名下的所有二级域名，这里也可以特指单个域名，例如a.test.com，单个域名后面可以使用免费的https的认证证书SSL。
   2. **源站信息**选择OSS域名可以联合2800多个阿里云OSS服务器，这里的OSS是指云对象存储，存储空间无上限，选择OSS域名选项后需要填对应的OSS域名地址，所以选这项时需要先开通OSS服务，OSS服务开通之后需要创建一个存储空间，创建存储空间时需要设置桶的名称，这名称一旦确定不可更改，区域也是一样的，其他的默认就可以了，因为经常使用的是标准存储，对于归档和低频是特殊存储，那两个存储类型可以在需要的时候开通，价格上都低于标准存储；创建好存储空间后选择存储空间再选择文件管理创建后面需要存储的文件夹。这一步还需要创建OSS的域名，在存储空间**概览**页面，单击**域名管理**页签，然后单击**绑定用户域名**，在**绑定用户域名**对话框设置以下项目。
3. **用户域名**：用于输入要绑定的域名名称，例如hello-world.com。最大输入 63 个字符。这里填写的域名需要填写到CDN的加速域名中才能起到加速访问的效果。
   4. **自动添加 CNAME 记录**：如果添加的域名是您当前阿里云账号下管理的域名，可以自动添加 CNAME 记录。如果添加的域名不是本账号下的域名，您需要在您的域名解析商处手动配置云解析，在云解析控制台下点击所选择的域名在**添加记录**对话框设置以下项目。这里我添加的是已有域名。
   5. **端口**默认80端口就可以
   6. **加速区域**看需要选



#### 开启HTTPS

1. 进入网址https://cdn.console.aliyun.com/overview
2. 选择**安全防护**->**证书服务**->**配置证书**
3. 这里是填写配置证书的信息
   1. 这里选择免费证书，同意授权就进行下一步
   2. 这里面需要选择之前配置的CDN加速域名，选择后就可以确定了





































