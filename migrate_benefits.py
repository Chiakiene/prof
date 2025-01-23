from main import app, db, SponsorshipTier, SponsorBenefit

def migrate_benefits():
    with app.app_context():
        # 全てのスポンサーシップティアを取得
        tiers = SponsorshipTier.query.all()
        
        for tier in tiers:
            if hasattr(tier, 'benefits') and tier.benefits:  # 古い benefits カラムがある場合
                # 特典を個別のレコードとして保存
                benefits = tier.benefits.split('\n')  # 改行で区切られていると仮定
                for benefit_text in benefits:
                    if benefit_text.strip():
                        benefit = SponsorBenefit(
                            tier_id=tier.id,
                            name=benefit_text.strip(),
                            description='',  # 必要に応じて設定
                            delivery_method='manual'  # デフォルト値
                        )
                        db.session.add(benefit)
        
        db.session.commit()

if __name__ == '__main__':
    migrate_benefits() 