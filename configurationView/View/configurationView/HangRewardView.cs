using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace configurationView
{
    public partial class HangRewardView : Form
    {
        MainForm main;
        JObject public_json_data;
        public HangRewardView(MainForm main, string hang_reward_path)
        {
            InitializeComponent();
            StartPosition = FormStartPosition.CenterScreen;
            this.main = main;
            StreamReader stream = File.OpenText(hang_reward_path);
            JsonTextReader reader = new JsonTextReader(stream);
            public_json_data = (JObject)JToken.ReadFrom(reader);
            stream.Close();
            reader.Close();
        }

        private void HangRewardView_FormClosing(object sender, FormClosingEventArgs e)
        {
            main.Show();
        }
    }
}
