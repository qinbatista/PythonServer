namespace configurationView
{
    partial class MainForm
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.label = new System.Windows.Forms.Label();
            this.panel1 = new System.Windows.Forms.Panel();
            this.comboBox5 = new System.Windows.Forms.ComboBox();
            this.IsPreWaveFinish = new System.Windows.Forms.CheckBox();
            this.label8 = new System.Windows.Forms.Label();
            this.WaveNumber = new System.Windows.Forms.NumericUpDown();
            this.comboBox1 = new System.Windows.Forms.ComboBox();
            this.numericUpDown3 = new System.Windows.Forms.NumericUpDown();
            this.label7 = new System.Windows.Forms.Label();
            this.button5 = new System.Windows.Forms.Button();
            this.button6 = new System.Windows.Forms.Button();
            this.button3 = new System.Windows.Forms.Button();
            this.button4 = new System.Windows.Forms.Button();
            this.comboBox4 = new System.Windows.Forms.ComboBox();
            this.comboBox3 = new System.Windows.Forms.ComboBox();
            this.label6 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.ColdDownTime = new System.Windows.Forms.NumericUpDown();
            this.label3 = new System.Windows.Forms.Label();
            this.TotalTime = new System.Windows.Forms.NumericUpDown();
            this.button2 = new System.Windows.Forms.Button();
            this.button1 = new System.Windows.Forms.Button();
            this.comboBox2 = new System.Windows.Forms.ComboBox();
            this.VersionOption = new System.Windows.Forms.ComboBox();
            this.add = new System.Windows.Forms.Button();
            this.FunctionOption = new System.Windows.Forms.ComboBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.dateTimePicker = new System.Windows.Forms.DateTimePicker();
            this.panel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.WaveNumber)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown3)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.ColdDownTime)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.TotalTime)).BeginInit();
            this.SuspendLayout();
            // 
            // label
            // 
            this.label.AutoSize = true;
            this.label.Location = new System.Drawing.Point(130, 31);
            this.label.Name = "label";
            this.label.Size = new System.Drawing.Size(44, 18);
            this.label.TabIndex = 0;
            this.label.Text = "版本";
            // 
            // panel1
            // 
            this.panel1.Controls.Add(this.comboBox5);
            this.panel1.Controls.Add(this.IsPreWaveFinish);
            this.panel1.Controls.Add(this.label8);
            this.panel1.Controls.Add(this.WaveNumber);
            this.panel1.Controls.Add(this.comboBox1);
            this.panel1.Controls.Add(this.numericUpDown3);
            this.panel1.Controls.Add(this.label7);
            this.panel1.Controls.Add(this.button5);
            this.panel1.Controls.Add(this.button6);
            this.panel1.Controls.Add(this.button3);
            this.panel1.Controls.Add(this.button4);
            this.panel1.Controls.Add(this.comboBox4);
            this.panel1.Controls.Add(this.comboBox3);
            this.panel1.Controls.Add(this.label6);
            this.panel1.Controls.Add(this.label5);
            this.panel1.Controls.Add(this.label4);
            this.panel1.Controls.Add(this.ColdDownTime);
            this.panel1.Controls.Add(this.label3);
            this.panel1.Controls.Add(this.TotalTime);
            this.panel1.Controls.Add(this.button2);
            this.panel1.Controls.Add(this.button1);
            this.panel1.Controls.Add(this.comboBox2);
            this.panel1.Location = new System.Drawing.Point(0, 191);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(1178, 505);
            this.panel1.TabIndex = 1;
            // 
            // comboBox5
            // 
            this.comboBox5.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox5.FormattingEnabled = true;
            this.comboBox5.Items.AddRange(new object[] {
            "Spawn1",
            "Spawn2",
            "Spawn3",
            "Spawn4",
            "Spawn5",
            "Spawn6",
            "Spawn7",
            "Spawn8",
            "Spawn9"});
            this.comboBox5.Location = new System.Drawing.Point(679, 393);
            this.comboBox5.Name = "comboBox5";
            this.comboBox5.Size = new System.Drawing.Size(360, 26);
            this.comboBox5.TabIndex = 29;
            // 
            // IsPreWaveFinish
            // 
            this.IsPreWaveFinish.AutoSize = true;
            this.IsPreWaveFinish.Location = new System.Drawing.Point(976, 171);
            this.IsPreWaveFinish.Name = "IsPreWaveFinish";
            this.IsPreWaveFinish.Size = new System.Drawing.Size(178, 22);
            this.IsPreWaveFinish.TabIndex = 28;
            this.IsPreWaveFinish.Text = "等待上一波怪打完";
            this.IsPreWaveFinish.UseVisualStyleBackColor = true;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(26, 172);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(80, 18);
            this.label8.TabIndex = 27;
            this.label8.Text = "第几波怪";
            // 
            // WaveNumber
            // 
            this.WaveNumber.Location = new System.Drawing.Point(112, 167);
            this.WaveNumber.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.WaveNumber.Name = "WaveNumber";
            this.WaveNumber.Size = new System.Drawing.Size(81, 28);
            this.WaveNumber.TabIndex = 26;
            this.WaveNumber.Value = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.WaveNumber.ValueChanged += new System.EventHandler(this.WaveNumber_ValueChanged);
            // 
            // comboBox1
            // 
            this.comboBox1.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox1.FormattingEnabled = true;
            this.comboBox1.Items.AddRange(new object[] {
            "普通关卡",
            "冲塔关卡"});
            this.comboBox1.Location = new System.Drawing.Point(29, 55);
            this.comboBox1.Name = "comboBox1";
            this.comboBox1.Size = new System.Drawing.Size(137, 26);
            this.comboBox1.TabIndex = 25;
            this.comboBox1.Tag = "";
            this.comboBox1.SelectedIndexChanged += new System.EventHandler(this.ComboBox1_SelectedIndexChanged);
            // 
            // numericUpDown3
            // 
            this.numericUpDown3.Location = new System.Drawing.Point(833, 279);
            this.numericUpDown3.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.numericUpDown3.Name = "numericUpDown3";
            this.numericUpDown3.Size = new System.Drawing.Size(81, 28);
            this.numericUpDown3.TabIndex = 24;
            this.numericUpDown3.Value = new decimal(new int[] {
            1,
            0,
            0,
            0});
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(765, 284);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(62, 18);
            this.label7.TabIndex = 23;
            this.label7.Text = "数量：";
            // 
            // button5
            // 
            this.button5.Location = new System.Drawing.Point(1075, 387);
            this.button5.Name = "button5";
            this.button5.Size = new System.Drawing.Size(79, 39);
            this.button5.TabIndex = 22;
            this.button5.Text = "添加";
            this.button5.UseVisualStyleBackColor = true;
            this.button5.Click += new System.EventHandler(this.Button5_Click);
            // 
            // button6
            // 
            this.button6.Location = new System.Drawing.Point(560, 387);
            this.button6.Name = "button6";
            this.button6.Size = new System.Drawing.Size(79, 39);
            this.button6.TabIndex = 21;
            this.button6.Text = "删除";
            this.button6.UseVisualStyleBackColor = true;
            this.button6.Click += new System.EventHandler(this.Button6_Click);
            // 
            // button3
            // 
            this.button3.Location = new System.Drawing.Point(1075, 274);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(79, 39);
            this.button3.TabIndex = 20;
            this.button3.Text = "添加";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.Button3_Click);
            // 
            // button4
            // 
            this.button4.Location = new System.Drawing.Point(960, 274);
            this.button4.Name = "button4";
            this.button4.Size = new System.Drawing.Size(79, 39);
            this.button4.TabIndex = 19;
            this.button4.Text = "删除";
            this.button4.UseVisualStyleBackColor = true;
            this.button4.Click += new System.EventHandler(this.Button4_Click);
            // 
            // comboBox4
            // 
            this.comboBox4.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox4.FormattingEnabled = true;
            this.comboBox4.Location = new System.Drawing.Point(161, 393);
            this.comboBox4.Name = "comboBox4";
            this.comboBox4.Size = new System.Drawing.Size(360, 26);
            this.comboBox4.TabIndex = 18;
            // 
            // comboBox3
            // 
            this.comboBox3.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox3.FormattingEnabled = true;
            this.comboBox3.Location = new System.Drawing.Point(161, 280);
            this.comboBox3.Name = "comboBox3";
            this.comboBox3.Size = new System.Drawing.Size(571, 26);
            this.comboBox3.TabIndex = 17;
            this.comboBox3.SelectedIndexChanged += new System.EventHandler(this.ComboBox3_SelectedIndexChanged);
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(26, 397);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(98, 18);
            this.label6.TabIndex = 16;
            this.label6.Text = "怪物生成点";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(26, 284);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(116, 18);
            this.label5.TabIndex = 15;
            this.label5.Text = "怪物生成列表";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(608, 172);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(170, 18);
            this.label4.TabIndex = 13;
            this.label4.Text = "每一波结束等待时间";
            // 
            // ColdDownTime
            // 
            this.ColdDownTime.Location = new System.Drawing.Point(784, 167);
            this.ColdDownTime.Name = "ColdDownTime";
            this.ColdDownTime.Size = new System.Drawing.Size(81, 28);
            this.ColdDownTime.TabIndex = 12;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(268, 172);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(170, 18);
            this.label3.TabIndex = 11;
            this.label3.Text = "每波怪的总生成时间";
            // 
            // TotalTime
            // 
            this.TotalTime.Location = new System.Drawing.Point(444, 167);
            this.TotalTime.Name = "TotalTime";
            this.TotalTime.Size = new System.Drawing.Size(81, 28);
            this.TotalTime.TabIndex = 10;
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(1075, 49);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(79, 39);
            this.button2.TabIndex = 9;
            this.button2.Text = "添加";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.Button2_Click);
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(960, 49);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(79, 39);
            this.button1.TabIndex = 8;
            this.button1.Text = "删除";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.Button1_Click);
            // 
            // comboBox2
            // 
            this.comboBox2.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox2.FormattingEnabled = true;
            this.comboBox2.Location = new System.Drawing.Point(216, 55);
            this.comboBox2.Name = "comboBox2";
            this.comboBox2.Size = new System.Drawing.Size(700, 26);
            this.comboBox2.TabIndex = 7;
            this.comboBox2.SelectedIndexChanged += new System.EventHandler(this.ComboBox2_SelectedIndexChanged);
            // 
            // VersionOption
            // 
            this.VersionOption.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.VersionOption.FormattingEnabled = true;
            this.VersionOption.Location = new System.Drawing.Point(216, 28);
            this.VersionOption.Name = "VersionOption";
            this.VersionOption.Size = new System.Drawing.Size(700, 26);
            this.VersionOption.TabIndex = 2;
            this.VersionOption.SelectedIndexChanged += new System.EventHandler(this.VersionOption_SelectedIndexChanged);
            // 
            // add
            // 
            this.add.Location = new System.Drawing.Point(960, 21);
            this.add.Name = "add";
            this.add.Size = new System.Drawing.Size(79, 39);
            this.add.TabIndex = 3;
            this.add.Text = "添加";
            this.add.UseVisualStyleBackColor = true;
            this.add.Click += new System.EventHandler(this.Add_Click);
            // 
            // FunctionOption
            // 
            this.FunctionOption.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.FunctionOption.FormattingEnabled = true;
            this.FunctionOption.Items.AddRange(new object[] {
            "普通关卡怪物生成：level_enemy_layouts_config",
            "塔怪物生成：level_enemy_layouts_config_tower",
            "怪物属性：monster_config",
            "进关消耗：entry_consumables_config",
            "挂机奖励：hang_reward_config",
            "抽奖奖励：lottery_config",
            "玩家配置表：player_config",
            "卷轴升级技能配置信息：skill_level_up_config",
            "通关奖励：stage_reward_config",
            "武器配置：weapon_config",
            "世界参数：world_distribution"});
            this.FunctionOption.Location = new System.Drawing.Point(216, 81);
            this.FunctionOption.Name = "FunctionOption";
            this.FunctionOption.Size = new System.Drawing.Size(700, 26);
            this.FunctionOption.TabIndex = 5;
            this.FunctionOption.SelectedIndexChanged += new System.EventHandler(this.FunctionOption_SelectedIndexChanged);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(130, 84);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(44, 18);
            this.label1.TabIndex = 4;
            this.label1.Text = "功能";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(130, 137);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(80, 18);
            this.label2.TabIndex = 6;
            this.label2.Text = "生效时间";
            // 
            // dateTimePicker
            // 
            this.dateTimePicker.Location = new System.Drawing.Point(262, 130);
            this.dateTimePicker.Name = "dateTimePicker";
            this.dateTimePicker.Size = new System.Drawing.Size(200, 28);
            this.dateTimePicker.TabIndex = 9;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 18F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1178, 694);
            this.Controls.Add(this.dateTimePicker);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.FunctionOption);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.add);
            this.Controls.Add(this.VersionOption);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.label);
            this.Name = "MainForm";
            this.RightToLeftLayout = true;
            this.Text = "View";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.WaveNumber)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown3)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.ColdDownTime)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.TotalTime)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.ComboBox VersionOption;
        private System.Windows.Forms.Button add;
        private System.Windows.Forms.ComboBox FunctionOption;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.DateTimePicker dateTimePicker;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown TotalTime;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.ComboBox comboBox2;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.NumericUpDown ColdDownTime;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.ComboBox comboBox4;
        private System.Windows.Forms.ComboBox comboBox3;
        private System.Windows.Forms.Button button5;
        private System.Windows.Forms.Button button6;
        private System.Windows.Forms.Button button3;
        private System.Windows.Forms.Button button4;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.NumericUpDown numericUpDown3;
        private System.Windows.Forms.ComboBox comboBox1;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.NumericUpDown WaveNumber;
        private System.Windows.Forms.CheckBox IsPreWaveFinish;
        private System.Windows.Forms.ComboBox comboBox5;
    }
}

