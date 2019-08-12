namespace configurationView
{
    partial class MonsterAdd
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.MonstersName = new System.Windows.Forms.ComboBox();
            this.label1 = new System.Windows.Forms.Label();
            this.button1 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.MonstersNumber = new System.Windows.Forms.NumericUpDown();
            ((System.ComponentModel.ISupportInitialize)(this.MonstersNumber)).BeginInit();
            this.SuspendLayout();
            // 
            // MonstersName
            // 
            this.MonstersName.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.MonstersName.FormattingEnabled = true;
            this.MonstersName.Items.AddRange(new object[] {
            "ZombieKid",
            "Enemy1"});
            this.MonstersName.Location = new System.Drawing.Point(125, 27);
            this.MonstersName.Name = "MonstersName";
            this.MonstersName.Size = new System.Drawing.Size(219, 26);
            this.MonstersName.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(21, 30);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(98, 18);
            this.label1.TabIndex = 1;
            this.label1.Text = "怪物名字：";
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(76, 148);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(88, 30);
            this.button1.TabIndex = 2;
            this.button1.Text = "添加";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.Button1_Click);
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(205, 148);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(88, 30);
            this.button2.TabIndex = 3;
            this.button2.Text = "取消";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.Button2_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(21, 90);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(98, 18);
            this.label2.TabIndex = 4;
            this.label2.Text = "怪物数量：";
            // 
            // MonstersNumber
            // 
            this.MonstersNumber.Location = new System.Drawing.Point(125, 80);
            this.MonstersNumber.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.MonstersNumber.Name = "MonstersNumber";
            this.MonstersNumber.Size = new System.Drawing.Size(81, 28);
            this.MonstersNumber.TabIndex = 13;
            this.MonstersNumber.Value = new decimal(new int[] {
            1,
            0,
            0,
            0});
            // 
            // MonsterAdd
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 18F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(371, 208);
            this.Controls.Add(this.MonstersNumber);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.button2);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.MonstersName);
            this.Name = "MonsterAdd";
            this.Text = "添加怪物";
            ((System.ComponentModel.ISupportInitialize)(this.MonstersNumber)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ComboBox MonstersName;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.NumericUpDown MonstersNumber;
    }
}