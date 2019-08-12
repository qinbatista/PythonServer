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
            this.Panel1 = new System.Windows.Forms.Panel();
            this.Panel1AddWave = new System.Windows.Forms.Button();
            this.Panel1DelWave = new System.Windows.Forms.Button();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.ColdDownTime = new System.Windows.Forms.NumericUpDown();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.TotalTime = new System.Windows.Forms.NumericUpDown();
            this.WaveNumber = new System.Windows.Forms.ComboBox();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.OptionalGenerationPoint = new System.Windows.Forms.ComboBox();
            this.Panel1AddPoint = new System.Windows.Forms.Button();
            this.Panel1Save = new System.Windows.Forms.Button();
            this.IsPreWaveFinish = new System.Windows.Forms.CheckBox();
            this.label8 = new System.Windows.Forms.Label();
            this.StageType = new System.Windows.Forms.ComboBox();
            this.MonsterAmount = new System.Windows.Forms.NumericUpDown();
            this.label7 = new System.Windows.Forms.Label();
            this.Panel1DelPoint = new System.Windows.Forms.Button();
            this.Panel1AddMonster = new System.Windows.Forms.Button();
            this.Panel1DelMonster = new System.Windows.Forms.Button();
            this.MonsterGenerationPoint = new System.Windows.Forms.ComboBox();
            this.MonsterList = new System.Windows.Forms.ComboBox();
            this.label6 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.Panel1AddStage = new System.Windows.Forms.Button();
            this.Panel1DelStage = new System.Windows.Forms.Button();
            this.StageNumber = new System.Windows.Forms.ComboBox();
            this.VersionOption = new System.Windows.Forms.ComboBox();
            this.AddVersion = new System.Windows.Forms.Button();
            this.FunctionOption = new System.Windows.Forms.ComboBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.dateTimePicker = new System.Windows.Forms.DateTimePicker();
            this.Panel2 = new System.Windows.Forms.Panel();
            this.Panel1.SuspendLayout();
            this.groupBox3.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.ColdDownTime)).BeginInit();
            this.groupBox2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.TotalTime)).BeginInit();
            this.groupBox1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.MonsterAmount)).BeginInit();
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
            // Panel1
            // 
            this.Panel1.Controls.Add(this.Panel1AddWave);
            this.Panel1.Controls.Add(this.Panel1DelWave);
            this.Panel1.Controls.Add(this.groupBox3);
            this.Panel1.Controls.Add(this.groupBox2);
            this.Panel1.Controls.Add(this.WaveNumber);
            this.Panel1.Controls.Add(this.groupBox1);
            this.Panel1.Controls.Add(this.Panel1Save);
            this.Panel1.Controls.Add(this.IsPreWaveFinish);
            this.Panel1.Controls.Add(this.label8);
            this.Panel1.Controls.Add(this.StageType);
            this.Panel1.Controls.Add(this.MonsterAmount);
            this.Panel1.Controls.Add(this.label7);
            this.Panel1.Controls.Add(this.Panel1DelPoint);
            this.Panel1.Controls.Add(this.Panel1AddMonster);
            this.Panel1.Controls.Add(this.Panel1DelMonster);
            this.Panel1.Controls.Add(this.MonsterGenerationPoint);
            this.Panel1.Controls.Add(this.MonsterList);
            this.Panel1.Controls.Add(this.label6);
            this.Panel1.Controls.Add(this.label5);
            this.Panel1.Controls.Add(this.Panel1AddStage);
            this.Panel1.Controls.Add(this.Panel1DelStage);
            this.Panel1.Controls.Add(this.StageNumber);
            this.Panel1.Location = new System.Drawing.Point(0, 191);
            this.Panel1.Name = "Panel1";
            this.Panel1.Size = new System.Drawing.Size(1178, 505);
            this.Panel1.TabIndex = 1;
            this.Panel1.Visible = false;
            // 
            // Panel1AddWave
            // 
            this.Panel1AddWave.Location = new System.Drawing.Point(1075, 147);
            this.Panel1AddWave.Name = "Panel1AddWave";
            this.Panel1AddWave.Size = new System.Drawing.Size(79, 39);
            this.Panel1AddWave.TabIndex = 35;
            this.Panel1AddWave.Text = "添加";
            this.Panel1AddWave.UseVisualStyleBackColor = true;
            this.Panel1AddWave.Click += new System.EventHandler(this.Panel1AddWave_Click);
            // 
            // Panel1DelWave
            // 
            this.Panel1DelWave.Location = new System.Drawing.Point(960, 147);
            this.Panel1DelWave.Name = "Panel1DelWave";
            this.Panel1DelWave.Size = new System.Drawing.Size(79, 39);
            this.Panel1DelWave.TabIndex = 34;
            this.Panel1DelWave.Text = "删除";
            this.Panel1DelWave.UseVisualStyleBackColor = true;
            this.Panel1DelWave.Click += new System.EventHandler(this.Panel1DelWave_Click);
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.ColdDownTime);
            this.groupBox3.Location = new System.Drawing.Point(497, 123);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(239, 69);
            this.groupBox3.TabIndex = 33;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "每一波结束等待时间(s)";
            // 
            // ColdDownTime
            // 
            this.ColdDownTime.Location = new System.Drawing.Point(48, 30);
            this.ColdDownTime.Name = "ColdDownTime";
            this.ColdDownTime.Size = new System.Drawing.Size(81, 28);
            this.ColdDownTime.TabIndex = 12;
            this.ColdDownTime.ValueChanged += new System.EventHandler(this.ColdDownTime_ValueChanged);
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.TotalTime);
            this.groupBox2.Location = new System.Drawing.Point(219, 123);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(251, 69);
            this.groupBox2.TabIndex = 32;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "每波怪的总生成时间(s)";
            // 
            // TotalTime
            // 
            this.TotalTime.Location = new System.Drawing.Point(52, 32);
            this.TotalTime.Name = "TotalTime";
            this.TotalTime.Size = new System.Drawing.Size(81, 28);
            this.TotalTime.TabIndex = 10;
            this.TotalTime.ValueChanged += new System.EventHandler(this.TotalTime_ValueChanged);
            // 
            // WaveNumber
            // 
            this.WaveNumber.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.WaveNumber.FormattingEnabled = true;
            this.WaveNumber.Location = new System.Drawing.Point(112, 152);
            this.WaveNumber.Name = "WaveNumber";
            this.WaveNumber.Size = new System.Drawing.Size(80, 26);
            this.WaveNumber.TabIndex = 31;
            this.WaveNumber.Tag = "";
            this.WaveNumber.SelectedIndexChanged += new System.EventHandler(this.WaveNumber_SelectedIndexChanged);
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.OptionalGenerationPoint);
            this.groupBox1.Controls.Add(this.Panel1AddPoint);
            this.groupBox1.Location = new System.Drawing.Point(684, 298);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(467, 67);
            this.groupBox1.TabIndex = 11;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "可选生成点";
            // 
            // OptionalGenerationPoint
            // 
            this.OptionalGenerationPoint.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.OptionalGenerationPoint.FormattingEnabled = true;
            this.OptionalGenerationPoint.Items.AddRange(new object[] {
            "Spawn1",
            "Spawn2",
            "Spawn3",
            "Spawn4",
            "Spawn5",
            "Spawn6",
            "Spawn7",
            "Spawn8",
            "Spawn9"});
            this.OptionalGenerationPoint.Location = new System.Drawing.Point(6, 35);
            this.OptionalGenerationPoint.Name = "OptionalGenerationPoint";
            this.OptionalGenerationPoint.Size = new System.Drawing.Size(349, 26);
            this.OptionalGenerationPoint.TabIndex = 29;
            // 
            // Panel1AddPoint
            // 
            this.Panel1AddPoint.Location = new System.Drawing.Point(388, 27);
            this.Panel1AddPoint.Name = "Panel1AddPoint";
            this.Panel1AddPoint.Size = new System.Drawing.Size(79, 39);
            this.Panel1AddPoint.TabIndex = 22;
            this.Panel1AddPoint.Text = "添加";
            this.Panel1AddPoint.UseVisualStyleBackColor = true;
            this.Panel1AddPoint.Click += new System.EventHandler(this.Panel1AddPoint_Click);
            // 
            // Panel1Save
            // 
            this.Panel1Save.Location = new System.Drawing.Point(345, 393);
            this.Panel1Save.Name = "Panel1Save";
            this.Panel1Save.Size = new System.Drawing.Size(550, 60);
            this.Panel1Save.TabIndex = 30;
            this.Panel1Save.Text = "保存";
            this.Panel1Save.UseVisualStyleBackColor = true;
            this.Panel1Save.Click += new System.EventHandler(this.Panel1Save_Click);
            // 
            // IsPreWaveFinish
            // 
            this.IsPreWaveFinish.AutoSize = true;
            this.IsPreWaveFinish.Location = new System.Drawing.Point(768, 154);
            this.IsPreWaveFinish.Name = "IsPreWaveFinish";
            this.IsPreWaveFinish.Size = new System.Drawing.Size(178, 22);
            this.IsPreWaveFinish.TabIndex = 28;
            this.IsPreWaveFinish.Text = "等待上一波怪打完";
            this.IsPreWaveFinish.UseVisualStyleBackColor = true;
            this.IsPreWaveFinish.CheckedChanged += new System.EventHandler(this.IsPreWaveFinish_CheckedChanged);
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(26, 157);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(80, 18);
            this.label8.TabIndex = 27;
            this.label8.Text = "第几波怪";
            // 
            // StageType
            // 
            this.StageType.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.StageType.FormattingEnabled = true;
            this.StageType.Items.AddRange(new object[] {
            "普通关卡",
            "冲塔关卡"});
            this.StageType.Location = new System.Drawing.Point(29, 55);
            this.StageType.Name = "StageType";
            this.StageType.Size = new System.Drawing.Size(137, 26);
            this.StageType.TabIndex = 25;
            this.StageType.Tag = "";
            this.StageType.SelectedIndexChanged += new System.EventHandler(this.StageType_SelectedIndexChanged);
            // 
            // MonsterAmount
            // 
            this.MonsterAmount.Location = new System.Drawing.Point(833, 237);
            this.MonsterAmount.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.MonsterAmount.Name = "MonsterAmount";
            this.MonsterAmount.Size = new System.Drawing.Size(81, 28);
            this.MonsterAmount.TabIndex = 24;
            this.MonsterAmount.ValueChanged += new System.EventHandler(this.MonsterAmount_ValueChanged);
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(765, 242);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(62, 18);
            this.label7.TabIndex = 23;
            this.label7.Text = "数量：";
            // 
            // Panel1DelPoint
            // 
            this.Panel1DelPoint.Location = new System.Drawing.Point(537, 326);
            this.Panel1DelPoint.Name = "Panel1DelPoint";
            this.Panel1DelPoint.Size = new System.Drawing.Size(79, 39);
            this.Panel1DelPoint.TabIndex = 21;
            this.Panel1DelPoint.Text = "删除";
            this.Panel1DelPoint.UseVisualStyleBackColor = true;
            this.Panel1DelPoint.Click += new System.EventHandler(this.Panel1DelPoint_Click);
            // 
            // Panel1AddMonster
            // 
            this.Panel1AddMonster.Location = new System.Drawing.Point(1075, 232);
            this.Panel1AddMonster.Name = "Panel1AddMonster";
            this.Panel1AddMonster.Size = new System.Drawing.Size(79, 39);
            this.Panel1AddMonster.TabIndex = 20;
            this.Panel1AddMonster.Text = "添加";
            this.Panel1AddMonster.UseVisualStyleBackColor = true;
            this.Panel1AddMonster.Click += new System.EventHandler(this.Panel1AddMonster_Click);
            // 
            // Panel1DelMonster
            // 
            this.Panel1DelMonster.Location = new System.Drawing.Point(960, 232);
            this.Panel1DelMonster.Name = "Panel1DelMonster";
            this.Panel1DelMonster.Size = new System.Drawing.Size(79, 39);
            this.Panel1DelMonster.TabIndex = 19;
            this.Panel1DelMonster.Text = "删除";
            this.Panel1DelMonster.UseVisualStyleBackColor = true;
            this.Panel1DelMonster.Click += new System.EventHandler(this.Panel1DelMonster_Click);
            // 
            // MonsterGenerationPoint
            // 
            this.MonsterGenerationPoint.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.MonsterGenerationPoint.FormattingEnabled = true;
            this.MonsterGenerationPoint.Location = new System.Drawing.Point(161, 332);
            this.MonsterGenerationPoint.Name = "MonsterGenerationPoint";
            this.MonsterGenerationPoint.Size = new System.Drawing.Size(360, 26);
            this.MonsterGenerationPoint.TabIndex = 18;
            // 
            // MonsterList
            // 
            this.MonsterList.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.MonsterList.FormattingEnabled = true;
            this.MonsterList.Location = new System.Drawing.Point(161, 238);
            this.MonsterList.Name = "MonsterList";
            this.MonsterList.Size = new System.Drawing.Size(571, 26);
            this.MonsterList.TabIndex = 17;
            this.MonsterList.SelectedIndexChanged += new System.EventHandler(this.MonsterList_SelectedIndexChanged);
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(26, 336);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(98, 18);
            this.label6.TabIndex = 16;
            this.label6.Text = "怪物生成点";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(26, 242);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(116, 18);
            this.label5.TabIndex = 15;
            this.label5.Text = "怪物生成列表";
            // 
            // Panel1AddStage
            // 
            this.Panel1AddStage.Location = new System.Drawing.Point(1075, 49);
            this.Panel1AddStage.Name = "Panel1AddStage";
            this.Panel1AddStage.Size = new System.Drawing.Size(79, 39);
            this.Panel1AddStage.TabIndex = 9;
            this.Panel1AddStage.Text = "添加";
            this.Panel1AddStage.UseVisualStyleBackColor = true;
            this.Panel1AddStage.Click += new System.EventHandler(this.Panel1AddStage_Click);
            // 
            // Panel1DelStage
            // 
            this.Panel1DelStage.Location = new System.Drawing.Point(960, 49);
            this.Panel1DelStage.Name = "Panel1DelStage";
            this.Panel1DelStage.Size = new System.Drawing.Size(79, 39);
            this.Panel1DelStage.TabIndex = 8;
            this.Panel1DelStage.Text = "删除";
            this.Panel1DelStage.UseVisualStyleBackColor = true;
            this.Panel1DelStage.Click += new System.EventHandler(this.Panel1DelStage_Click);
            // 
            // StageNumber
            // 
            this.StageNumber.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.StageNumber.FormattingEnabled = true;
            this.StageNumber.Location = new System.Drawing.Point(216, 55);
            this.StageNumber.Name = "StageNumber";
            this.StageNumber.Size = new System.Drawing.Size(700, 26);
            this.StageNumber.TabIndex = 7;
            this.StageNumber.SelectedIndexChanged += new System.EventHandler(this.StageNumber_SelectedIndexChanged);
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
            // AddVersion
            // 
            this.AddVersion.Location = new System.Drawing.Point(960, 21);
            this.AddVersion.Name = "AddVersion";
            this.AddVersion.Size = new System.Drawing.Size(79, 39);
            this.AddVersion.TabIndex = 3;
            this.AddVersion.Text = "添加";
            this.AddVersion.UseVisualStyleBackColor = true;
            this.AddVersion.Click += new System.EventHandler(this.AddVersion_Click);
            // 
            // FunctionOption
            // 
            this.FunctionOption.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.FunctionOption.FormattingEnabled = true;
            this.FunctionOption.Items.AddRange(new object[] {
            "怪物生成设置",
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
            // Panel2
            // 
            this.Panel2.Location = new System.Drawing.Point(592, 130);
            this.Panel2.Name = "Panel2";
            this.Panel2.Size = new System.Drawing.Size(36, 26);
            this.Panel2.TabIndex = 10;
            this.Panel2.Visible = false;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 18F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1178, 694);
            this.Controls.Add(this.Panel1);
            this.Controls.Add(this.Panel2);
            this.Controls.Add(this.dateTimePicker);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.FunctionOption);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.AddVersion);
            this.Controls.Add(this.VersionOption);
            this.Controls.Add(this.label);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "MainForm";
            this.RightToLeftLayout = true;
            this.Text = "View";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.Panel1.ResumeLayout(false);
            this.Panel1.PerformLayout();
            this.groupBox3.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.ColdDownTime)).EndInit();
            this.groupBox2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.TotalTime)).EndInit();
            this.groupBox1.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.MonsterAmount)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label;
        private System.Windows.Forms.Panel Panel1;
        private System.Windows.Forms.ComboBox VersionOption;
        private System.Windows.Forms.Button AddVersion;
        private System.Windows.Forms.ComboBox FunctionOption;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.DateTimePicker dateTimePicker;
        private System.Windows.Forms.NumericUpDown TotalTime;
        private System.Windows.Forms.Button Panel1AddStage;
        private System.Windows.Forms.Button Panel1DelStage;
        private System.Windows.Forms.ComboBox StageNumber;
        private System.Windows.Forms.NumericUpDown ColdDownTime;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.ComboBox MonsterGenerationPoint;
        private System.Windows.Forms.ComboBox MonsterList;
        private System.Windows.Forms.Button Panel1AddPoint;
        private System.Windows.Forms.Button Panel1DelPoint;
        private System.Windows.Forms.Button Panel1AddMonster;
        private System.Windows.Forms.Button Panel1DelMonster;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.NumericUpDown MonsterAmount;
        private System.Windows.Forms.ComboBox StageType;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.CheckBox IsPreWaveFinish;
        private System.Windows.Forms.ComboBox OptionalGenerationPoint;
        private System.Windows.Forms.Button Panel1Save;
        private System.Windows.Forms.Panel Panel2;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.ComboBox WaveNumber;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.Button Panel1AddWave;
        private System.Windows.Forms.Button Panel1DelWave;
    }
}

