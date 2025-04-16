from datetime import datetime
import numpy as np
class AIAnalyzer:
    def __init__(self):
        pass
        
    def analyze_stock(self, stock_data, fundamental_data):
        try:
            # Her bir AI modelinin analizi
            technical_ai = self._technical_analysis_ai(stock_data)
            fundamental_ai = self._fundamental_analysis_ai(fundamental_data)
            volume_ai = self._volume_analysis_ai(stock_data)
            
            return {
                "teknik_uzman": technical_ai,
                "temel_uzman": fundamental_ai,
                "hacim_uzmani": volume_ai
            }
            
        except Exception as e:
            return {
                "error": f"AI analizi sırasında hata oluştu: {str(e)}"
            }
    
    def _technical_analysis_ai(self, data):
        """Teknik analiz yapan AI"""
        signals = []
        
        # RSI Analizi
        if data.get('RSI', 0) < 30:
            signals.append("RSI aşırı satım bölgesinde, alım fırsatı olabilir")
        elif data.get('RSI', 0) > 70:
            signals.append("RSI aşırı alım bölgesinde, satış fırsatı olabilir")
            
        # MACD Analizi    
        if data.get('MACD', 0) > data.get('MACD_signal', 0):
            signals.append("MACD pozitif sinyal veriyor")
        else:
            signals.append("MACD negatif sinyal veriyor")
            
        # Ortalama Analizleri
        price = data.get('son_fiyat', 0)
        if price > data.get('EMA_20', 0):
            signals.append("Fiyat 20 günlük ortalamanın üzerinde")
        else:
            signals.append("Fiyat 20 günlük ortalamanın altında")
        return "Teknik Analiz Uzmanı: " + " ve ".join(signals)
    def _fundamental_analysis_ai(self, data):
        """Temel analiz yapan AI"""
        signals = []
        
        # F/K Analizi
        fk = data.get('F/K', 0)
        if isinstance(fk, (int, float)):
            if fk < 10:
                signals.append("F/K oranı düşük, hisse değerli olabilir")
            elif fk > 20:
                signals.append("F/K oranı yüksek, hisse pahalı olabilir")
                
        # Temettü Analizi
        temettu = data.get('Temettu Verimi', '0%')
        if isinstance(temettu, str) and '%' in temettu:
            temettu_oran = float(temettu.replace('%', ''))
            if temettu_oran > 5:
                signals.append("Yüksek temettü verimi var")
                
        return "Temel Analiz Uzmanı: " + " ve ".join(signals) if signals else "Temel Analiz Uzmanı: Yeterli veri yok"
    def _volume_analysis_ai(self, data):
        """Hacim analizi yapan AI"""
        current_volume = data.get('Volume', 0)
        avg_volume = np.mean([data.get('Volume', 0)] * 20)  # Son 20 günlük ortalama
        
        if current_volume > avg_volume * 2:
            return "Hacim Uzmanı: Anormal yüksek hacim, önemli bir hareket olabilir"
        elif current_volume > avg_volume * 1.5:
            return "Hacim Uzmanı: Hacimde artış var, trend güçlenebilir"
        else:
            return "Hacim Uzmanı: Hacim normal seviyede"