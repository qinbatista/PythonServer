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

namespace configurationView
{
    public partial class MonsterAdd : Form
    {
        JArray array;
        public MonsterAdd(JArray array)
        {
            InitializeComponent();
            this.array = array;
        }

        private void Button1_Click(object sender, EventArgs e)
        {
            try
            {
                MessageBox.Show(array.ToString());
                array.Add(JToken.Parse(String.Format("{\"count\": 1,\"enemysPrefString\": \"{0}\"}", comboBox1.SelectedItem.ToString())));
                MessageBox.Show(array.ToString());
            }
            catch
            {
                MessageBox.Show(text: "没有选择怪物类型！", caption: "错误提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
