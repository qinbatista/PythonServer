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
        JObject client_stage_json;
        public MonsterAdd(JObject client_stage_json)
        {
            InitializeComponent();
            this.client_stage_json = client_stage_json;
        }

        private void Button1_Click(object sender, EventArgs e)
        {
            //add_item = comboBox1.SelectedItem.ToString();
            MessageBox.Show(text: client_stage_json.ToString());
            //client_stage_json.Add("client_stage_json": client_stage_json["client_stage_json"][0]);
            textBox1.Text = client_stage_json.ToString();
        }
    }
}
