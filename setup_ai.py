#!/usr/bin/env python3
"""AI Provider Setup - Install and configure free AI providers"""
import sys, subprocess, json, os, urllib.request

sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("  AI Provider Setup - ربط مزود الذكاء الاصطناعي")
print("=" * 60)
print("""
اختر مزود AI:

  1. Ollama (محلي، مجاني بالكامل) - موصى به
     - Llama 3.2, Mistral, وغيرها
     - يعمل بدون إنترنت بعد التحميل
     - لا يحتاج أي مفتاح API

  2. Groq (سحابي، مجاني)
     - Llama 3 70B، Mixtral
     - سريع جداً، 30 طلب/دقيقة مجاناً
     - يحتاج مفتاح API مجاني من groq.com

  3. OpenAI (سحابي، مدفوع)
     - GPT-4o, GPT-4
     - الأقوى ولكن بمقابل مادي
     - يحتاج مفتاح API من platform.openai.com

  4. الوضع الحالي (بدون AI) - البيانات الاحتياطية
""")

choice = input("اختيار (1/2/3/4): ").strip()

if choice == "1":
    print("\nجارٍ التحقق من Ollama...")
    try:
        r = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3)
        models = json.loads(r.read())
        print(f"  ✅ Ollama يعمل - الموديلات المتاحة:")
        for m in models.get("models", []):
            print(f"     - {m['name']}")
    except Exception:
        print("  ❌ Ollama غير مثبت")
        print("\nلتثبيت Ollama:")
        print("  1. افتح https://ollama.com/download/windows")
        print("  2. حمّل المثبت ونفذه")
        print("  3. بعد التثبيت، شغّل:")
        print("     ollama pull llama3.2")
        print("\nأو استخدم الخيار 2 (Groq) كبديل فوري.")

elif choice == "2":
    print("\nللحصول على مفتاح Groq API المجاني:")
    print("  1. افتح https://console.groq.com/keys")
    print("  2. سجّل أو سجّل الدخول")
    print("  3. انقر 'Create API Key'")
    print("  4. انسخ المفتاح")
    key = input("\nالصق مفتاح Groq API: ").strip()
    if key:
        env_path = os.path.join(os.path.dirname(__file__), "backend", ".env")
        with open(env_path, "a") as f:
            f.write(f"\nGROQ_API_KEY={key}\n")
        print(f"  ✅ تم حفظ المفتاح في {env_path}")
        print("  أعد تشغيل الخادم لتفعيل Groq")

elif choice == "3":
    key = input("الصق مفتاح OpenAI API: ").strip()
    if key:
        env_path = os.path.join(os.path.dirname(__file__), "backend", ".env")
        with open(env_path, "a") as f:
            f.write(f"\nOPENAI_API_KEY={key}\n")
        print(f"  ✅ تم حفظ المفتاح في {env_path}")

elif choice == "4":
    print("  ✅ الوضع الحالي: البيانات الاحتياطية الذكية مفعلة")
    print("     النظام يعمل ولكن بدون ذكاء اصطناعي حقيقي")

print()
print("=" * 60)
print("  ملخص مزود AI الحالي:")
settings_path = os.path.join(os.path.dirname(__file__), "backend", ".env")
if os.path.exists(settings_path):
    with open(settings_path) as f:
        for line in f:
            line = line.strip()
            if "API_KEY" in line or "api_key" in line or "PROVIDER" in line:
                val = line.split("=", 1)[1] if "=" in line else ""
                if val and val != "None":
                    print(f"  ✅ {line.split('=')[0]} = {val[:20]}...")
                else:
                    print(f"  ⚠️  {line}")

print()
print("الخادم يستخدم الآن MultiAIService الذي يدعم:")
print("  OpenAI → Groq → Ollama → Smart Fallback")
print("(يحاول بالترتيب ويستخدم أول مزود متاح)")
print("=" * 60)
