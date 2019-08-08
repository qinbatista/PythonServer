using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.IO;
using Microsoft.VisualBasic;

namespace configurationView
{
    public partial class Form1 : Form
    {
        //DirectoryInfo di1 = new DirectoryInfo(Directory.GetCurrentDirectory());
        static string main_path = "..//..//..//..//..//configuration//";
        string json_version = main_path + "config_timer_setting.json";
        StreamReader stream;
        JsonTextReader reader;
        JObject json;
        public Form1()
        {
            InitializeComponent();
            stream = File.OpenText(json_version);
            reader = new JsonTextReader(stream);
            json = (JObject)JToken.ReadFrom(reader);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            foreach(var date in json)
            {
                //this.VersionOption.Items.Add(date.Key + ":" + date.Value);
                this.VersionOption.Items.Add(date.Value["server"]);
            }
        }
        private void Add_Click(object sender, EventArgs e)
        {
            String version_str = Interaction.InputBox("请输入版本号，将会拷贝最新版本作为当前版本", "输入密码", "");
            try
            {
                float version = float.Parse(version_str);
                DialogResult result = MessageBox.Show(text: "是否确定使用版本号：" + version_str, caption: "确认提示", MessageBoxButtons.YesNo, MessageBoxIcon.Information);
                if (result.ToString().Equals("Yes"))
                {
                    this.FunctionOption.Items.Add(version);
                }
            }
            catch
            {
                MessageBox.Show(text: "版本信息输入错误！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
