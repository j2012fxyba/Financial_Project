from flask import Flask, render_template, request, jsonify

app = Flask('web',static_folder='D:\\tool\\PythonTest\\flask\\flask_templates\\static',
            template_folder='D:\\tool\\PythonTest\\flask\\flask_templates\\templates')

@app.route('/')
def index():
    return render_template('bmi_calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        height = float(data['height']) / 100  # 转换为米
        weight = float(data['weight'])
        
        if height <= 0 or weight <= 0:
            return jsonify({'error': '身高和体重必须为正数'}), 400
            
        bmi = weight / (height ** 2)
        bmi_rounded = round(bmi, 1)
        
        # 判断BMI分类
        if bmi < 18.5:
            category = '偏瘦'
            advice = '建议适当增加营养摄入，保持适度运动'
        elif 18.5 <= bmi < 24:
            category = '正常'
            advice = '保持良好生活习惯，继续维持健康体重'
        elif 24 <= bmi < 28:
            category = '超重'
            advice = '建议控制饮食，增加运动量'
        else:
            category = '肥胖'
            advice = '建议咨询医生或营养师，制定减重计划'
        
        return jsonify({
            'bmi': bmi_rounded,
            'category': category,
            'advice': advice
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.debug=True
app.run()