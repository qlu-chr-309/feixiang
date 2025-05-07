<template>
	<view class="register-container">
		<view class="header">
			<view class="back-btn" @click="goBack">
				<text class="iconfont icon-back"></text>
			</view>
			<view class="header-title">赛事报名</view>
		</view>
		
		<scroll-view scroll-y class="content-scroll">
			<view class="event-info">
				<image :src="eventData.image" mode="aspectFill" class="event-image"></image>
				<view class="event-detail">
					<text class="event-title">{{eventData.title}}</text>
					<view class="event-meta">
						<view class="meta-item">
							<text class="iconfont icon-time"></text>
							<text>{{eventData.time}}</text>
						</view>
						<view class="meta-item">
							<text class="iconfont icon-location"></text>
							<text>{{eventData.location}}</text>
						</view>
					</view>
				</view>
			</view>
			
			<view class="form-section">
				<view class="section-title">报名信息</view>
				
				<view class="form-item">
					<text class="form-label">参赛类别</text>
					<view class="radio-group">
						<view class="radio-item" @click="formData.type = 'personal'">
							<view class="radio" :class="{ active: formData.type === 'personal' }"></view>
							<text>个人赛 (¥200)</text>
						</view>
						<view class="radio-item" @click="formData.type = 'team'">
							<view class="radio" :class="{ active: formData.type === 'team' }"></view>
							<text>团队赛 (¥500)</text>
						</view>
					</view>
				</view>
				
				<view class="form-item">
					<text class="form-label">姓名</text>
					<input type="text" v-model="formData.name" placeholder="请输入真实姓名" class="form-input" />
				</view>
				
				<view class="form-item">
					<text class="form-label">手机号码</text>
					<input type="number" v-model="formData.phone" placeholder="请输入手机号码" class="form-input" />
				</view>
				
				<view class="form-item">
					<text class="form-label">身份证号</text>
					<input type="idcard" v-model="formData.idCard" placeholder="请输入身份证号码" class="form-input" />
				</view>
				
				<view class="form-item" v-if="formData.type === 'team'">
					<text class="form-label">团队名称</text>
					<input type="text" v-model="formData.teamName" placeholder="请输入团队名称" class="form-input" />
				</view>
				
				<view class="form-item" v-if="formData.type === 'team'">
					<text class="form-label">团队人数</text>
					<view class="number-input">
						<view class="number-btn minus" @click="decreaseNumber">-</view>
						<input type="number" v-model="formData.teamCount" class="number-value" />
						<view class="number-btn plus" @click="increaseNumber">+</view>
					</view>
				</view>
				
				<view class="form-item">
					<text class="form-label">电子邮箱</text>
					<input type="text" v-model="formData.email" placeholder="请输入电子邮箱" class="form-input" />
				</view>
				
				<view class="form-item textarea-item">
					<text class="form-label">无人机设备</text>
					<textarea v-model="formData.equipment" placeholder="请填写您计划使用的无人机型号及其配件" class="form-textarea"></textarea>
				</view>
				
				<view class="form-item textarea-item">
					<text class="form-label">无人机经验</text>
					<textarea v-model="formData.experience" placeholder="请简单描述您的无人机飞行经验" class="form-textarea"></textarea>
				</view>
			</view>
			
			<view class="form-section">
				<view class="section-title">支付信息</view>
				
				<view class="form-item">
					<text class="form-label">支付方式</text>
					<view class="payment-methods">
						<view class="payment-item" @click="formData.paymentMethod = 'wechat'">
							<view class="payment-icon wechat">
								<text class="iconfont icon-wechat"></text>
							</view>
							<text class="payment-name">微信支付</text>
							<view class="payment-check" :class="{ active: formData.paymentMethod === 'wechat' }"></view>
						</view>
						<view class="payment-item" @click="formData.paymentMethod = 'alipay'">
							<view class="payment-icon alipay">
								<text class="iconfont icon-alipay"></text>
							</view>
							<text class="payment-name">支付宝</text>
							<view class="payment-check" :class="{ active: formData.paymentMethod === 'alipay' }"></view>
						</view>
					</view>
				</view>
				
				<view class="price-detail">
					<view class="price-item">
						<text>报名费用</text>
						<text>¥{{getPrice()}}</text>
					</view>
					<view class="price-item">
						<text>优惠券</text>
						<text class="discount">-¥0</text>
					</view>
					<view class="price-total">
						<text>实付款</text>
						<text class="total-price">¥{{getPrice()}}</text>
					</view>
				</view>
			</view>
			
			<view class="agreement">
				<view class="checkbox" :class="{ active: formData.agreement }" @click="formData.agreement = !formData.agreement"></view>
				<text>我已阅读并同意<text class="link">《报名协议》</text>和<text class="link">《免责声明》</text></text>
			</view>
			
			<button class="submit-btn" :disabled="!formData.agreement" @click="submitRegistration">提交报名</button>
		</scroll-view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				id: 0,
				eventData: {
					id: 1,
					title: '2023年全国无人机创新应用大赛',
					time: '2023-05-20 ~ 2023-05-22',
					location: '深圳市南山区科技园',
					image: '/static/community/event1.jpg'
				},
				formData: {
					type: 'personal',
					name: '',
					phone: '',
					idCard: '',
					teamName: '',
					teamCount: 2,
					email: '',
					equipment: '',
					experience: '',
					paymentMethod: 'wechat',
					agreement: false
				}
			};
		},
		onLoad(options) {
			if (options.id) {
				this.id = options.id;
				// 这里应该根据id从服务器获取赛事详情
				// 这里使用模拟数据
			}
		},
		methods: {
			goBack() {
				uni.navigateBack();
			},
			getPrice() {
				return this.formData.type === 'personal' ? 200 : 500;
			},
			increaseNumber() {
				if (this.formData.teamCount < 5) {
					this.formData.teamCount++;
				} else {
					uni.showToast({
						title: '团队人数最多5人',
						icon: 'none'
					});
				}
			},
			decreaseNumber() {
				if (this.formData.teamCount > 2) {
					this.formData.teamCount--;
				} else {
					uni.showToast({
						title: '团队人数最少2人',
						icon: 'none'
					});
				}
			},
			validateForm() {
				if (!this.formData.name) {
					uni.showToast({
						title: '请输入姓名',
						icon: 'none'
					});
					return false;
				}
				
				if (!this.formData.phone) {
					uni.showToast({
						title: '请输入手机号码',
						icon: 'none'
					});
					return false;
				}
				
				if (!this.formData.idCard) {
					uni.showToast({
						title: '请输入身份证号码',
						icon: 'none'
					});
					return false;
				}
				
				if (this.formData.type === 'team' && !this.formData.teamName) {
					uni.showToast({
						title: '请输入团队名称',
						icon: 'none'
					});
					return false;
				}
				
				if (!this.formData.equipment) {
					uni.showToast({
						title: '请填写无人机设备信息',
						icon: 'none'
					});
					return false;
				}
				
				if (!this.formData.agreement) {
					uni.showToast({
						title: '请阅读并同意报名协议',
						icon: 'none'
					});
					return false;
				}
				
				return true;
			},
			submitRegistration() {
				if (!this.validateForm()) return;
				
				uni.showLoading({
					title: '提交中...'
				});
				
				// 模拟提交
				setTimeout(() => {
					uni.hideLoading();
					uni.showModal({
						title: '报名成功',
						content: '您已成功报名参加2023年全国无人机创新应用大赛',
						showCancel: false,
						success: (res) => {
							if (res.confirm) {
								uni.navigateBack({
									delta: 2 // 返回上上页，即赛事列表页
								});
							}
						}
					});
				}, 1500);
			}
		}
	}
</script>

<style>
	.register-container {
		min-height: 100vh;
		background-color: #f5f5f5;
	}
	
	.header {
		background-color: #007AFF;
		padding: 20rpx 30rpx;
		color: #fff;
		display: flex;
		align-items: center;
		position: relative;
	}
	
	.back-btn {
		position: absolute;
		left: 30rpx;
	}
	
	.header-title {
		flex: 1;
		font-size: 36rpx;
		font-weight: bold;
		text-align: center;
	}
	
	.content-scroll {
		height: calc(100vh - 80rpx);
		padding-bottom: 40rpx;
	}
	
	.event-info {
		background-color: #fff;
		display: flex;
		padding: 20rpx;
		margin-bottom: 20rpx;
	}
	
	.event-image {
		width: 200rpx;
		height: 150rpx;
		border-radius: 8rpx;
		margin-right: 20rpx;
	}
	
	.event-detail {
		flex: 1;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
	
	.event-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 10rpx;
	}
	
	.event-meta {
		font-size: 26rpx;
		color: #666;
	}
	
	.meta-item {
		display: flex;
		align-items: center;
		margin-bottom: 10rpx;
	}
	
	.meta-item .iconfont {
		margin-right: 10rpx;
		color: #999;
	}
	
	.form-section {
		background-color: #fff;
		padding: 30rpx;
		margin-bottom: 20rpx;
	}
	
	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 30rpx;
		position: relative;
		padding-left: 20rpx;
	}
	
	.section-title::before {
		content: '';
		position: absolute;
		left: 0;
		top: 8rpx;
		width: 8rpx;
		height: 32rpx;
		background-color: #007AFF;
		border-radius: 4rpx;
	}
	
	.form-item {
		margin-bottom: 30rpx;
	}
	
	.form-label {
		font-size: 28rpx;
		color: #333;
		margin-bottom: 15rpx;
		display: block;
	}
	
	.form-input {
		width: 100%;
		height: 80rpx;
		background-color: #f5f5f5;
		border-radius: 8rpx;
		padding: 0 20rpx;
		font-size: 28rpx;
		color: #333;
	}
	
	.form-textarea {
		width: 100%;
		height: 180rpx;
		background-color: #f5f5f5;
		border-radius: 8rpx;
		padding: 20rpx;
		font-size: 28rpx;
		color: #333;
	}
	
	.radio-group {
		display: flex;
	}
	
	.radio-item {
		display: flex;
		align-items: center;
		margin-right: 40rpx;
	}
	
	.radio {
		width: 40rpx;
		height: 40rpx;
		border-radius: 20rpx;
		border: 2rpx solid #ddd;
		margin-right: 10rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.radio.active {
		border-color: #007AFF;
	}
	
	.radio.active::after {
		content: '';
		width: 24rpx;
		height: 24rpx;
		border-radius: 12rpx;
		background-color: #007AFF;
	}
	
	.number-input {
		display: flex;
		align-items: center;
	}
	
	.number-btn {
		width: 80rpx;
		height: 80rpx;
		background-color: #f5f5f5;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 40rpx;
		color: #333;
	}
	
	.number-btn.minus {
		border-radius: 8rpx 0 0 8rpx;
	}
	
	.number-btn.plus {
		border-radius: 0 8rpx 8rpx 0;
	}
	
	.number-value {
		width: 100rpx;
		height: 80rpx;
		background-color: #f5f5f5;
		text-align: center;
		font-size: 28rpx;
		color: #333;
	}
	
	.payment-methods {
		display: flex;
		justify-content: space-between;
	}
	
	.payment-item {
		flex: 1;
		height: 150rpx;
		background-color: #f5f5f5;
		border-radius: 8rpx;
		margin: 0 10rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		position: relative;
	}
	
	.payment-item:first-child {
		margin-left: 0;
	}
	
	.payment-item:last-child {
		margin-right: 0;
	}
	
	.payment-icon {
		width: 64rpx;
		height: 64rpx;
		border-radius: 32rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 10rpx;
	}
	
	.payment-icon.wechat {
		background-color: #09bb07;
		color: #fff;
	}
	
	.payment-icon.alipay {
		background-color: #00a0e9;
		color: #fff;
	}
	
	.payment-name {
		font-size: 26rpx;
		color: #333;
	}
	
	.payment-check {
		position: absolute;
		right: 20rpx;
		top: 20rpx;
		width: 36rpx;
		height: 36rpx;
		border-radius: 18rpx;
		border: 2rpx solid #ddd;
	}
	
	.payment-check.active {
		border-color: #007AFF;
		background-color: #007AFF;
	}
	
	.payment-check.active::after {
		content: '';
		position: absolute;
		left: 12rpx;
		top: 6rpx;
		width: 10rpx;
		height: 16rpx;
		border-right: 4rpx solid #fff;
		border-bottom: 4rpx solid #fff;
		transform: rotate(45deg);
	}
	
	.price-detail {
		background-color: #f5f5f5;
		border-radius: 8rpx;
		padding: 20rpx;
		margin-top: 30rpx;
	}
	
	.price-item {
		display: flex;
		justify-content: space-between;
		margin-bottom: 15rpx;
		font-size: 28rpx;
		color: #666;
	}
	
	.discount {
		color: #ff4d4f;
	}
	
	.price-total {
		display: flex;
		justify-content: space-between;
		padding-top: 15rpx;
		border-top: 1rpx solid #eee;
		font-size: 32rpx;
		color: #333;
		font-weight: bold;
	}
	
	.total-price {
		color: #ff4d4f;
	}
	
	.agreement {
		display: flex;
		align-items: center;
		padding: 20rpx 30rpx;
		font-size: 26rpx;
		color: #666;
	}
	
	.checkbox {
		width: 36rpx;
		height: 36rpx;
		border-radius: 8rpx;
		border: 2rpx solid #ddd;
		margin-right: 10rpx;
		position: relative;
	}
	
	.checkbox.active {
		background-color: #007AFF;
		border-color: #007AFF;
	}
	
	.checkbox.active::after {
		content: '';
		position: absolute;
		left: 12rpx;
		top: 6rpx;
		width: 10rpx;
		height: 16rpx;
		border-right: 4rpx solid #fff;
		border-bottom: 4rpx solid #fff;
		transform: rotate(45deg);
	}
	
	.link {
		color: #007AFF;
	}
	
	.submit-btn {
		width: 90%;
		height: 90rpx;
		line-height: 90rpx;
		background-color: #007AFF;
		color: #fff;
		font-size: 32rpx;
		border-radius: 45rpx;
		margin: 30rpx auto 60rpx;
	}
	
	.submit-btn[disabled] {
		background-color: #ccc;
		color: #fff;
	}
</style> 