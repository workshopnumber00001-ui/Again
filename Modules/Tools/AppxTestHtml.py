async def generate_Mock_HTML(FileName, Time, Marks, Questions, jsonData):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{FileName}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {{
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --secondary: #0ea5e9;
            --success: #22c55e;
            --danger: #ef4444;
            --warning: #f59e0b;
            --text: #1e293b;
            --text-light: #64748b;
            --bg: #f8fafc;
            --card: #ffffff;
            --border: #e2e8f0;
            --sidebar-width: 280px;

            /* Dark mode variables */
            --dark-bg: #0f172a;
            --dark-card: #1e293b;
            --dark-text: #f1f5f9;
            --dark-text-light: #94a3b8;
            --dark-border: #334155;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
            font-size: 16px;
        }}

        body {{
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.5;
            transition: all 0.3s ease;
            min-height: 100vh;
        }}

        body.dark-mode {{
            background-color: var(--dark-bg);
            color: var(--dark-text);
        }}

        .container {{
            display: flex;
            min-height: calc(100vh - 60px);
            padding: 1rem;
            margin-top: 60px;
        }}

        /* Header Styles */
        .test-header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
            background-color: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 0.75rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-bottom: 1px solid var(--border);
            height: 60px;
        }}

        .dark-mode .test-header {{
            background-color: rgba(30, 41, 59, 0.95);
            border-bottom-color: var(--dark-border);
        }}

        .test-title {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .topic-name {{
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .test-name {{
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--primary);
            letter-spacing: -0.025em;
        }}

        .header-controls {{
            display: flex;
            gap: 1rem;
            align-items: center;
        }}

        .theme-toggle {{
            background: none;
            border: none;
            color: var(--text);
            font-size: 1.25rem;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 0.5rem;
            transition: all 0.2s;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .dark-mode .theme-toggle {{
            color: var(--dark-text);
        }}

        .theme-toggle:hover {{
            background-color: var(--bg);
        }}

        .dark-mode .theme-toggle:hover {{
            background-color: var(--dark-card);
        }}

        /* Question Styles */
        .question-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background-color: var(--card);
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            width: 100%;
        }}

        .dark-mode .question-container {{
            background-color: var(--dark-card);
        }}

        .question-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }}

        .question-info {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        .question-timer {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            color: var(--text-light);
        }}

        .question-number {{
            font-size: 1rem;
            color: var(--text-light);
            font-weight: 500;
        }}

        .question-text {{
            font-size: 1rem;
            margin-bottom: 1.5rem;
            line-height: 1.6;
            color: var(--text);
        }}

        .dark-mode .question-text {{
            color: var(--dark-text);
        }}

        .options-container {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .option {{
            padding: 1.25rem;
            border: 2px solid var(--border);
            border-radius: 0.75rem;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 1rem;
            user-select: none;
        }}

        .dark-mode .option {{
            border-color: var(--dark-border);
            color: var(--dark-text);
        }}

        .option:hover {{
            border-color: var(--primary);
            transform: translateY(-1px);
        }}

        .option.selected {{
            background-color: var(--primary);
            color: white;
            border-color: var(--primary);
        }}

        .option-marker {{
            width: 28px;
            height: 28px;
            border: 2px solid var(--border);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.875rem;
            font-weight: 600;
            flex-shrink: 0;
            background-color: var(--bg);
            color: var(--text);
        }}

        .dark-mode .option-marker {{
            border-color: var(--dark-border);
            background-color: var(--dark-bg);
            color: var(--dark-text);
        }}

        .option.selected .option-marker {{
            background-color: white;
            color: var(--primary);
            border-color: white;
        }}

        .navigation-buttons {{
            display: flex;
            justify-content: space-between;
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border);
            gap: 0.5rem;
            flex-wrap: wrap;
        }}

        .dark-mode .navigation-buttons {{
            border-top-color: var(--dark-border);
        }}

        .nav-btn {{
            padding: 0.75rem 1rem;
            border: none;
            border-radius: 0.75rem;
            background-color: var(--primary);
            color: white;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 600;
            font-size: 0.875rem;
            min-width: 100px;
            justify-content: center;
            flex: 1;
        }}

        .nav-btn:hover {{
            background-color: var(--primary-dark);
            transform: translateY(-1px);
        }}

        .nav-btn:disabled {{
            background-color: var(--text-light);
            cursor: not-allowed;
            transform: none;
            opacity: 0.7;
        }}

        @media (max-width: 768px) {{
            .navigation-buttons {{
                padding: 1rem 0;
                gap: 0.5rem;
            }}

            .nav-btn {{
                padding: 0.5rem 0.75rem;
                min-width: auto;
                font-size: 0.75rem;
                flex: 1 1 calc(50% - 0.5rem);
            }}

            .nav-btn i {{
                font-size: 0.75rem;
            }}

            .nav-btn:first-child,
            .nav-btn:last-child {{
                flex: 1 1 100%;
                order: -1;
            }}
        }}

        /* Timer styles */
        .timer-container {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--primary);
            color: white;
            padding: 0.75rem 1.25rem;
            border-radius: 0.75rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            z-index: 1000;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .timer-warning {{
            background: var(--warning) !important;
        }}

        .timer-danger {{
            background: var(--danger) !important;
            animation: blink 1s infinite;
        }}

        @keyframes blink {{
            50% {{ opacity: 0.7; }}
        }}

        .dark-mode .timer-container {{
            color: var(--dark-text);
        }}

        /* Progress bar */
        .progress-container {{
            width: 100%;
            height: 4px;
            background-color: var(--border);
            position: fixed;
            top: 60px;
            left: 0;
            z-index: 99;
        }}

        .dark-mode .progress-container {{
            background-color: var(--dark-border);
        }}

        .progress-bar {{
            height: 100%;
            background-color: var(--primary);
            width: 0%;
            transition: width 0.3s ease;
        }}

        /* Results Analysis Styles */
        .results-container {{
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.9);
            display: none;
            justify-content: center;
            align-items: flex-start;
            z-index: 2000;
            padding: 2rem;
            backdrop-filter: blur(8px);
            overflow-y: auto;
        }}

        .results-card {{
            position: relative;
            background: var(--card);
            border-radius: 1.5rem;
            padding: 3rem;
            max-width: 1000px;
            width: 100%;
            margin: 2rem auto;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            border: 1px solid var(--border);
        }}

        .dark-mode .results-card {{
            background: var(--dark-card);
            border-color: var(--dark-border);
        }}

        .results-header {{
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 2px solid var(--border);
            position: relative;
        }}

        .results-header::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 2px;
            background: var(--primary);
        }}

        .results-header h2 {{
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 1rem;
            font-weight: 700;
            letter-spacing: -0.025em;
        }}

        .results-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 4rem;
        }}

        .stat-card {{
            background: var(--bg);
            padding: 2rem;
            border-radius: 1.25rem;
            text-align: center;
            border: 1px solid var(--border);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--primary);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }}

        .stat-card:hover::before {{
            opacity: 1;
        }}

        .dark-mode .stat-card {{
            background: var(--dark-card);
            border-color: var(--dark-border);
        }}

        .stat-value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 1rem;
            line-height: 1;
            font-feature-settings: "tnum";
        }}

        .stat-label {{
            font-size: 0.875rem;
            color: var(--text-light);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .question-review {{
            margin-top: 3rem;
        }}

        .question-review-header {{
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }}

        .question-review-header h3 {{
            font-size: 1.25rem;
            color: var(--text);
            font-weight: 600;
        }}

        .dark-mode .question-review-header h3 {{
            color: var(--dark-text);
        }}

        .review-item {{
            background: var(--card);
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border);
            transition: transform 0.2s ease;
        }}

        .review-item:hover {{
            transform: translateY(-2px);
        }}

        .dark-mode .review-item {{
            background: var(--dark-card);
            border-color: var(--dark-border);
        }}

        .review-item.correct {{
            border-left: 4px solid var(--success);
        }}

        .review-item.incorrect {{
            border-left: 4px solid var(--danger);
        }}

        .review-item.unattempted {{
            border-left: 4px solid var(--text-light);
        }}

        .review-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }}

        .review-header h4 {{
            font-size: 1rem;
            font-weight: 600;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .dark-mode .review-header h4 {{
            color: var(--dark-text);
        }}

        .review-status {{
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            font-size: 0.875rem;
            font-weight: 500;
        }}

        .review-status.correct {{
            background: rgba(34, 197, 94, 0.1);
            color: var(--success);
        }}

        .review-status.incorrect {{
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
        }}

        .review-status.unattempted {{
            background: rgba(100, 116, 139, 0.1);
            color: var(--text-light);
        }}

        .close-results {{
            position: fixed;
            top: 1.5rem;
            right: 1.5rem;
            background: var(--primary);
            border: none;
            color: white;
            font-size: 1.25rem;
            cursor: pointer;
            padding: 0.75rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 3000;
        }}

        .close-results:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        }}

        .dark-mode .close-results {{
            background: var(--primary-dark);
        }}

        @media (max-width: 768px) {{
            * {{
                font-size: 14px;
            }}

            .container {{
                padding: 0.5rem;
            }}

            .question-container {{
                padding: 1rem;
                border-radius: 0.75rem;
                margin-bottom: 80px;
            }}

            .option {{
                padding: 0.875rem;
            }}

            .navigation-buttons {{
                padding: 1rem 0;
                gap: 0.5rem;
            }}

            .nav-btn {{
                padding: 0.75rem 1rem;
                min-width: auto;
                font-size: 0.875rem;
            }}

            .timer-container {{
                bottom: 20px;
                right: 50%;
                transform: translateX(50%);
                font-size: 0.875rem;
                padding: 0.5rem 1rem;
            }}

            .test-header {{
                padding: 0.75rem 1rem;
            }}

            .test-title {{
                font-size: 1rem;
            }}

            .question-text {{
                font-size: 0.95rem;
            }}

            .option-text {{
                font-size: 0.9rem;
            }}

            .option-marker {{
                width: 24px;
                height: 24px;
                font-size: 0.8rem;
            }}

            .results-card {{
                padding: 1.5rem;
                margin: 1rem;
            }}

            .stat-card {{
                padding: 1rem;
            }}

            .stat-value {{
                font-size: 1.5rem;
            }}

            .review-item {{
                padding: 1rem;
            }}
        }}

        /* Question palette styles */
        .question-palette {{
            position: fixed;
            right: 20px;
            top: 80px;
            background: var(--card);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid var(--border);
            max-width: 300px;
            display: none;
            z-index: 50;
        }}

        .palette-status-summary {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }}

        .status-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem;
            border-radius: 0.5rem;
            background: var(--bg);
            border: 1px solid var(--border);
            font-size: 0.875rem;
        }}

        .status-item .count {{
            font-weight: 600;
            color: var(--primary);
            min-width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--card);
            border-radius: 50%;
        }}

        .status-item.answered {{
            border-left: 3px solid var(--success);
        }}

        .status-item.not-answered {{
            border-left: 3px solid var(--danger);
        }}

        .status-item.review {{
            border-left: 3px solid var(--warning);
        }}

        .status-item.bookmarked {{
            border-left: 3px solid var(--primary);
        }}

        .dark-mode .status-item {{
            background: var(--dark-card);
            border-color: var(--dark-border);
        }}

        .dark-mode .status-item .count {{
            background: var(--dark-bg);
            color: var(--dark-text);
        }}

        @media (max-width: 768px) {{
            .palette-status-summary {{
                grid-template-columns: repeat(2, 1fr);
                gap: 0.5rem;
                margin-bottom: 1rem;
            }}

            .status-item {{
                padding: 0.375rem;
                font-size: 0.75rem;
            }}

            .status-item .count {{
                min-width: 20px;
                height: 20px;
                font-size: 0.75rem;
            }}
        }}

        @media (min-width: 1200px) {{
            .question-palette {{
                display: block;
            }}

            .container {{
                margin-right: 320px;
            }}
        }}

        .dark-mode .question-palette {{
            background: var(--dark-card);
            border-color: var(--dark-border);
        }}

        .palette-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 0.5rem;
            margin-top: 1rem;
        }}

        .palette-item {{
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid var(--border);
            border-radius: 0.5rem;
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 600;
            transition: all 0.2s;
            user-select: none;
        }}

        .dark-mode .palette-item {{
            border-color: var(--dark-border);
        }}

        .palette-item:hover {{
            border-color: var(--primary);
            transform: translateY(-1px);
        }}

        .palette-item.answered {{
            background: var(--success);
            color: white;
            border-color: var(--success);
        }}

        .palette-item.bookmarked {{
            background: #9333ea;
            color: white;
            border-color: #9333ea;
        }}

        .palette-item.current {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }}

        .palette-item.review {{
            background: var(--warning);
            color: white;
            border-color: var(--warning);
        }}

        .palette-item.answered.review {{
            background: linear-gradient(135deg, var(--success) 50%, var(--warning) 50%);
            color: white;
            border-color: var(--warning);
        }}
        .palette-item.answered.bookmarked {{
            background: linear-gradient(135deg, var(--success) 50%, #9333ea 50%);
            color: white;
            border-color: #9333ea;
        }}

        .palette-item.bookmarked.review {{
            background: linear-gradient(135deg, #9333ea 50%, var(--warning) 50%);
            color: white;
            border-color: var(--warning);
        }}

        .palette-item.answered.bookmarked.review {{
            background: linear-gradient(135deg, var(--success) 33%, #9333ea 33%, #9333ea 66%, var(--warning) 66%);
            color: white;
            border-color: var(--warning);
        }}

        @media (max-width: 768px) {{
            .question-palette {{
                position: fixed;
                top: auto;
                bottom: 80px;
                left: 0;
                right: 0;
                max-width: 100%;
                margin: 0 12px;
                padding: 0.75rem;
                display: none;
                z-index: 49;
                border-radius: 0.75rem;
            }}

            .palette-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(32px, 1fr));
                gap: 0.35rem;
            }}

            .palette-item {{
                width: 100%;
                height: 32px;
                font-size: 0.75rem;
                border-radius: 0.375rem;
                border-width: 1px;
            }}

            .palette-toggle {{
                position: fixed;
                bottom: 16px;
                left: 16px;
                padding: 0.4rem;
                border-radius: 0.375rem;
                width: 36px;
                height: 36px;
            }}

            .palette-toggle i {{
                font-size: 1.1rem;
            }}

            .question-palette h3 {{
                font-size: 0.9rem;
                margin-bottom: 0.5rem;
            }}

            .palette-legend {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin-bottom: 0.5rem;
                font-size: 0.7rem;
            }}

            .legend-item {{
                display: flex;
                align-items: center;
                gap: 0.25rem;
            }}

            .legend-color {{
                width: 12px;
                height: 12px;
                border-radius: 3px;
            }}
        }}

        @media (max-width: 768px) {{
            .bookmark-btn, 
            .review-btn {{
                width: 32px;
                height: 32px;
                font-size: 1rem;
                padding: 0.35rem;
            }}

            .bookmark-indicator {{
                font-size: 1rem;
            }}
        }}

        .bookmark-btn {{
            background: none;
            border: none;
            color: var(--text);
            font-size: 1.25rem;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 0.5rem;
            transition: all 0.2s;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .dark-mode .bookmark-btn {{
            color: var(--dark-text);
        }}

        .bookmark-btn:hover {{
            background-color: var(--bg);
        }}

        .dark-mode .bookmark-btn:hover {{
            background-color: var(--dark-card);
        }}

        .bookmark-btn.active {{
            background-color: var(--primary);
            color: white;
        }}

        .dark-mode .bookmark-btn.active {{
            background-color: var(--primary-dark);
        }}

        .bookmark-indicator {{
            color: var(--warning);
            font-size: 1.125rem;
        }}

        .user-info {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-right: 1rem;
        }}

        .user-logo {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
        }}

        .user-details {{
            display: flex;
            flex-direction: column;
        }}

        .user-name {{
            font-weight: 600;
            color: var(--primary);
        }}

        .telegram-link {{
            color: var(--text-light);
            text-decoration: none;
            font-size: 0.875rem;
            display: flex;
            align-items: center;
            gap: 0.25rem;
            transition: color 0.2s;
        }}

        .telegram-link:hover {{
            color: var(--primary);
        }}

        .dark-mode .user-name {{
            color: var(--dark-text);
        }}

        .dark-mode .telegram-link {{
            color: var(--dark-text-light);
        }}

        .dark-mode .telegram-link:hover {{
            color: var(--primary);
        }}

        @media (max-width: 768px) {{
            .user-info {{
                display: none;
            }}
        }}

        .results-filter {{
            display: flex;
            gap: 0.75rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            justify-content: center;
        }}

        .filter-btn {{
            padding: 0.6rem 1.2rem;
            border: none;
            background: var(--bg);
            color: var(--text);
            border-radius: 2rem;
            font-weight: 500;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 2px solid var(--border);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}

        .filter-btn i {{
            font-size: 0.9rem;
            width: 1em;
            text-align: center;
        }}

        .dark-mode .filter-btn {{
            background: var(--dark-card);
            border-color: var(--dark-border);
            color: var(--dark-text);
        }}

        .filter-btn:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-color: var(--primary);
        }}

        .filter-btn.active {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }}
        .filter-btn.active i {{
            color: white;
        }}
        .filter-btn[onclick*="correct"] {{
            border-color: var(--success);
        }}

        .filter-btn[onclick*="correct"] i {{
            color: var(--success);
        }}

        .filter-btn[onclick*="incorrect"] {{
            border-color: var(--danger);
        }}

        .filter-btn[onclick*="incorrect"] i {{
            color: var(--danger);
        }}

        .filter-btn[onclick*="unattempted"] {{
            border-color: var(--text-light);
        }}

        .filter-btn[onclick*="unattempted"] i {{
            color: var(--text-light);
        }}

        @media (max-width: 768px) {{
            .results-filter {{
                gap: 0.5rem;
            }}

            .filter-btn {{
                padding: 0.5rem 1rem;
                font-size: 0.8rem;
            }}
        }}

        .no-items-message {{
            text-align: center;
            padding: 2rem;
            color: var(--text-light);
            font-size: 0.9rem;
            background: var(--bg);
            border-radius: 0.5rem;
            margin: 1rem 0;
            display: none;
        }}

        .dark-mode .no-items-message {{
            background: var(--dark-card);
        }}

        .results-filter {{
            position: relative;
            z-index: 1;
        }}

        .filter-btn {{
            position: relative;
            overflow: hidden;
        }}

        .filter-btn:active {{
            transform: translateY(1px);
        }}

        @media (max-width: 768px) {{
            .results-filter {{
                padding: 0.5rem;
                margin: -0.5rem;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: none;
                -ms-overflow-style: none;
            }}

            .results-filter::-webkit-scrollbar {{
                display: none;
            }}

            .filter-btn {{
                white-space: nowrap;
                flex-shrink: 0;
            }}
        }}
    </style>
    <script>
    window.MathJax = {{
        tex: {{ inlineMath: [['\\\\(', '\\\\)'], ['$$', '$$']] }},
        svg: {{ fontCache: 'global' }}
    }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
    <div class="progress-container">
        <div id="progressBar" class="progress-bar"></div>
    </div>

    <div class="test-header">
        <div class="test-title">
            <div class="topic-name">MOCK TEST</div>
            <div class="test-name">{FileName} QUESTION-{Questions}, MARKS-{Marks}, TIME-{Time}</div>
        </div>
        <div class="header-controls">
            <div class="user-info">
                <img src="https://envs.sh/E7.jpg" alt="Megatron Logo" class="user-logo">
                <div class="user-details">
                    <div class="user-name">『 𝗠ᴇɢᴀᴛʀᴏɴ 🧑‍💻 』</div>
                    <a href="https://t.me/megatron2466" class="telegram-link" target="_blank">
                        <i class="fab fa-telegram"></i> @megatron2466
                    </a>
                </div>
            </div>
            <button class="theme-toggle" onclick="toggleTheme()" title="Toggle theme">
                <i class="fas fa-moon"></i>
            </button>
        </div>
    </div>

    <div class="timer-container">
        <i class="fas fa-clock"></i>
        <span id="timer">00:00:00</span>
    </div>

    <div class="results-container" id="resultsContainer">
        <button class="close-results" onclick="closeResults()">
            <i class="fas fa-times"></i>
        </button>
        <div class="results-card">
            <div class="results-header">
                <h2>Test Results</h2>
            </div>
            <div class="results-stats" id="resultsStats">
                <!-- Stats will be populated here -->
            </div>
            <div class="question-review" id="questionReview">
                <!-- Question review will be populated here -->
            </div>
        </div>
    </div>

    <div class="container">
        <div id="questionContainer" class="question-container">
            <!-- Questions will be loaded here -->
        </div>
    </div>

    <div class="question-palette" id="questionPalette">
        <div class="palette-status-summary">
            <div class="status-item answered">
                <span class="count" id="answeredCount">0</span>
                <span>Answered</span>
            </div>
            <div class="status-item not-answered">
                <span class="count" id="notAnsweredCount">0</span>
                <span>Not Answered</span>
            </div>
            <div class="status-item review">
                <span class="count" id="reviewCount">0</span>
                <span>For Review</span>
            </div>
            <div class="status-item bookmarked">
                <span class="count" id="bookmarkedCount">0</span>
                <span>Bookmarked</span>
            </div>
        </div>
        <h3>Question Palette</h3>
        <div class="palette-grid" id="paletteGrid"></div>
    </div>

    <button class="palette-toggle" onclick="togglePalette()" title="Toggle question palette">
        <i class="fas fa-th"></i>
    </button>

    <script>
        // Test configuration
        const TOTAL_TIME_MINUTES = {Time};
        const MAX_MARKS = {Marks};
        const NEGATIVE_MARKING_FACTOR = 0.25; // 1/4th negative marking
        
        // Questions data
        const questions = {jsonData};
        let currentQuestionIndex = 0;
        let userAnswers = new Array(questions.length).fill(null);
        let bookmarkedQuestions = new Set();
        let timeLeft;
        let timerInterval;
        let reviewedQuestions = new Set();
        let questionTimers = new Array(questions.length).fill(0); // Track time spent on each question
        let currentQuestionStartTime; // To track when a question was opened

        // Initialize timer
        function startTimer() {{
            timeLeft = TOTAL_TIME_MINUTES * 60;
            updateTimer(); // Update immediately
            timerInterval = setInterval(updateTimer, 1000);
            
            // Start the current question timer
            startQuestionTimer();
        }}

        function startQuestionTimer() {{
            // Record start time for current question
            currentQuestionStartTime = Date.now();
            
            // Initialize display
            updateQuestionTimerDisplay();
            
            // Update the timer display every second
            if (window.questionTimerInterval) {{
                clearInterval(window.questionTimerInterval);
            }}
            
            window.questionTimerInterval = setInterval(() => {{
                updateQuestionTimerDisplay();
            }}, 1000);
        }}
        
        function updateQuestionTimerDisplay() {{
            const elapsedSeconds = Math.floor((Date.now() - currentQuestionStartTime) / 1000) + questionTimers[currentQuestionIndex];
            const minutes = Math.floor(elapsedSeconds / 60);
            const seconds = elapsedSeconds % 60;
            
            const questionTimerElement = document.getElementById('questionTimer');
            if (questionTimerElement) {{
                questionTimerElement.textContent = `${{minutes.toString().padStart(2, '0')}}:${{seconds.toString().padStart(2, '0')}}`;
            }}
        }}

        function pauseQuestionTimer() {{
            if (window.questionTimerInterval) {{
                clearInterval(window.questionTimerInterval);
                
                // Calculate time spent on this question and store it
                const timeSpent = Math.floor((Date.now() - currentQuestionStartTime) / 1000);
                questionTimers[currentQuestionIndex] += timeSpent;
                
                currentQuestionStartTime = null; // Reset start time
            }}
        }}

        function updateTimer() {{
            if (timeLeft <= 0) {{
                clearInterval(timerInterval);
                if (window.questionTimerInterval) {{
                    clearInterval(window.questionTimerInterval);
                }}
                showResults();
                return;
            }}
            
            timeLeft--;
            const hours = Math.floor(timeLeft / 3600);
            const minutes = Math.floor((timeLeft % 3600) / 60);
            const seconds = timeLeft % 60;
            
            const timerElement = document.getElementById('timer');
            timerElement.textContent = 
                `${{hours.toString().padStart(2, '0')}}:${{minutes.toString().padStart(2, '0')}}:${{seconds.toString().padStart(2, '0')}}`;
            
            // Add warning colors
            const timerContainer = document.querySelector('.timer-container');
            timerContainer.classList.remove('timer-warning', 'timer-danger');
            
            if (timeLeft <= 300) {{ // Last 5 minutes
                timerContainer.classList.add('timer-danger');
            }} else if (timeLeft <= 600) {{ // Last 10 minutes
                timerContainer.classList.add('timer-warning');
            }}
        }}

        function calculateScore() {{
            let score = 0;
            const marksPerQuestion = MAX_MARKS / questions.length;
            
            userAnswers.forEach((answer, index) => {{
                if (answer !== null) {{
                    if (answer.toString() === questions[index].answer) {{
                        score += marksPerQuestion;
                    }} else {{
                        score -= marksPerQuestion * NEGATIVE_MARKING_FACTOR;
                    }}
                }}
            }});
            
            return Math.max(0, score);
        }}

        function showResults() {{
            // Pause the current question timer when showing results
            pauseQuestionTimer();
            clearInterval(timerInterval);
            if (window.questionTimerInterval) {{
                clearInterval(window.questionTimerInterval);
            }}
            
            const resultsContainer = document.getElementById('resultsContainer');
            
            // Calculate stats
            let correct = 0;
            let incorrect = 0;
            let unattempted = 0;
            let bookmarked = bookmarkedQuestions.size;
            
            userAnswers.forEach((answer, index) => {{
                if (answer === null) {{
                    unattempted++;
                }} else if (answer.toString() === questions[index].answer) {{
                    correct++;
                }} else {{
                    incorrect++;
                }}
            }});
            
            const finalScore = calculateScore();
            const accuracy = correct > 0 ? ((correct / (correct + incorrect)) * 100).toFixed(1) : 0;
            const attempted = correct + incorrect;
            const attemptRate = ((attempted / questions.length) * 100).toFixed(1);
            
            // Update stats
            const statsContainer = document.getElementById('resultsStats');
            statsContainer.innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${{finalScore.toFixed(2)}}</div>
                    <div class="stat-label"><i class="fas fa-star"></i> Total Score</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${{accuracy}}%</div>
                    <div class="stat-label"><i class="fas fa-bullseye"></i> Accuracy</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${{correct}}</div>
                    <div class="stat-label"><i class="fas fa-check-circle"></i> Correct</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${{incorrect}}</div>
                    <div class="stat-label"><i class="fas fa-times-circle"></i> Incorrect</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${{attemptRate}}%</div>
                    <div class="stat-label"><i class="fas fa-tasks"></i> Attempt Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${{bookmarked}}</div>
                    <div class="stat-label"><i class="fas fa-bookmark"></i> Bookmarked</div>
                </div>
            `;
            
            // Display question review with time spent per question
            const reviewContainer = document.getElementById('questionReview');
            reviewContainer.innerHTML = `
                <div class="question-review-header">
                    <h3>Detailed Analysis</h3>
                    <div class="results-filter">
                        <button class="filter-btn active" onclick="filterReviewItems('all')">
                            <i class="fas fa-list"></i> All Questions
                        </button>
                        <button class="filter-btn" onclick="filterReviewItems('correct')">
                            <i class="fas fa-check"></i> Correct
                        </button>
                        <button class="filter-btn" onclick="filterReviewItems('incorrect')">
                            <i class="fas fa-times"></i> Incorrect
                        </button>
                        <button class="filter-btn" onclick="filterReviewItems('unattempted')">
                            <i class="fas fa-minus"></i> Unattempted
                        </button>
                    </div>
                </div>
                ${{questions.map((q, index) => {{
                    const isCorrect = userAnswers[index]?.toString() === q.answer;
                    const isBookmarked = bookmarkedQuestions.has(index);
                    const status = userAnswers[index] === null ? 'unattempted' : 
                                 isCorrect ? 'correct' : 'incorrect';
                    
                    const statusIcon = status === 'correct' ? 'check-circle' :
                                     status === 'incorrect' ? 'times-circle' : 'minus-circle';
                    
                    // Format time spent on question
                    const timeSpent = questionTimers[index];
                    const timeMinutes = Math.floor(timeSpent / 60);
                    const timeSeconds = timeSpent % 60;
                    
                    return `
                        <div class="review-item ${{status}}" data-status="${{status}}">
                            <div class="review-header">
                                <h4>
                                    Question ${{index + 1}}
                                    ${{isBookmarked ? '<i class="fas fa-bookmark" style="color: var(--warning);"></i>' : ''}}
                                    <span style="color: var(--text-light); font-size: 0.875rem;">
                                        <i class="fas fa-clock"></i>
                                        ${{timeMinutes}}:${{timeSeconds.toString().padStart(2, '0')}}
                                    </span>
                                </h4>
                                <span class="review-status ${{status}}">
                                    <i class="fas fa-${{statusIcon}}"></i>
                                    ${{status.charAt(0).toUpperCase() + status.slice(1)}}
                                </span>
                                <button class="review-toggle" onclick="toggleReviewContent(this)" title="Expand/Collapse">
                                    <i class="fas fa-chevron-down"></i>
                                </button>
                            </div>
                            <div class="review-content">
                                <div class="review-question">${{q.question}}</div>
                                <div class="review-answer">
                                    <strong><i class="fas fa-user"></i> Your Answer</strong>
                                    <div>${{userAnswers[index] === null ? 'Not attempted' : q['option_' + userAnswers[index]]}}</div>
                                </div>
                                <div class="review-correct">
                                    <strong><i class="fas fa-check"></i> Correct Answer</strong>
                                    <div>${{q['option_' + q.answer]}}</div>
                                </div>
                                <div class="review-solution">
                                    <strong><i class="fas fa-lightbulb"></i> ${{q.solution_heading || 'Solution'}}</strong>
                                    <div>${{q.solution_text || 'No solution provided'}}</div>
                                </div>
                            </div>
                        </div>
                    `;
                }}).join('')}}
            `;
            
            // Show the results container
            resultsContainer.style.display = 'flex';

            // ✅ Fix math rendering in options too
            if (window.MathJax) {{
               MathJax.typesetPromise();
            }}
        }}

        function closeResults() {{
            document.getElementById('resultsContainer').style.display = 'none';
        }}

        function navigateToQuestion(index) {{
            currentQuestionIndex = index;
            displayQuestion(index);
        }}

        function displayQuestion(index) {{
            const question = questions[index];
            const container = document.getElementById('questionContainer');
            
            container.innerHTML = `
                <div class="question-header">
                    <div class="question-info">
                        <div class="question-number">Question ${{index + 1}} of ${{questions.length}}</div>
                    </div>
                    <button class="bookmark-btn ${{bookmarkedQuestions.has(index) ? 'active' : ''}}" onclick="toggleBookmark()" title="Bookmark this question">
                        <i class="fas fa-bookmark"></i>
                    </button>
                </div>
                <div class="question-text">${{question.question}}</div>
                <div class="options-container">
                    ${{[1, 2, 3, 4].map(optionNum => `
                        <div class="option ${{userAnswers[index] === optionNum ? 'selected' : ''}}" 
                             onclick="selectOption(${{optionNum}})"
                             role="button"
                             tabindex="0">
                            <div class="option-marker">${{String.fromCharCode(64 + optionNum)}}</div>
                            <div class="option-text">${{question['option_' + optionNum]}}</div>
                        </div>
                    `).join('')}}
                </div>
                <div class="navigation-buttons">
                    <button class="nav-btn" 
                            onclick="previousQuestion()" 
                            ${{index === 0 ? 'disabled' : ''}}>
                        <i class="fas fa-arrow-left"></i>
                        Previous
                    </button>
                    <button class="nav-btn" onclick="clearSelection()">
                        <i class="fas fa-eraser"></i>
                        Mark as Clear
                    </button>
                    <button class="nav-btn" onclick="markAsReview()">
                        <i class="fas fa-flag"></i>
                        Mark for Review
                    </button>
                    ${{index === questions.length - 1 ? 
                        `<button class="nav-btn" onclick="showResults()">
                            <i class="fas fa-flag-checkered"></i>
                            Submit Test
                        </button>` :
                        `<button class="nav-btn" onclick="nextQuestion()">
                            Next
                            <i class="fas fa-arrow-right"></i>
                        </button>`
                    }}
                </div>
            `;

            const progress = ((index + 1) / questions.length) * 100;
            document.getElementById('progressBar').style.width = `${{progress}}%`;
            updatePalette();
            
            // ✅ Fix math rendering in options too
            if (window.MathJax) {{
               MathJax.typesetPromise();
			}}
        }}

        function selectOption(optionNum) {{
            userAnswers[currentQuestionIndex] = optionNum;
            displayQuestion(currentQuestionIndex);
        }}

        function nextQuestion() {{
            if (currentQuestionIndex < questions.length - 1) {{
                currentQuestionIndex++;
                displayQuestion(currentQuestionIndex);
            }}
        }}

        function previousQuestion() {{
            if (currentQuestionIndex > 0) {{
                currentQuestionIndex--;
                displayQuestion(currentQuestionIndex);
            }}
        }}

        function toggleTheme() {{
            document.body.classList.toggle('dark-mode');
            const themeIcon = document.querySelector('.theme-toggle i');
            if (document.body.classList.contains('dark-mode')) {{
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
            }} else {{
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
            }}
        }}

        function togglePalette() {{
            const palette = document.getElementById('questionPalette');
            if (palette.style.display === 'none' || !palette.style.display) {{
                palette.style.display = 'block';
            }} else {{
                palette.style.display = 'none';
            }}
        }}

        function updatePalette() {{
            const paletteGrid = document.getElementById('paletteGrid');
            paletteGrid.innerHTML = '';
            // Initialize counters
            let answeredCount = 0;
            let notAnsweredCount = questions.length;
            let reviewCount = 0;
            let bookmarkedCount = 0;
            
            for (let i = 0; i < questions.length; i++) {{
                const item = document.createElement('div');
                item.className = 'palette-item';
                if (i === currentQuestionIndex) item.classList.add('current');
                if (userAnswers[i] !== null) {{
                    item.classList.add('answered');
                    answeredCount++;
                    notAnsweredCount--;
                }}
                if (bookmarkedQuestions.has(i)) {{
                    item.classList.add('bookmarked');
                    bookmarkedCount++;
                }}
                if (reviewedQuestions && reviewedQuestions.has(i)) {{
                    item.classList.add('review');
                    reviewCount++;
                }}
                item.textContent = i + 1;
                item.onclick = () => navigateToQuestion(i);
                paletteGrid.appendChild(item);
            }}
            // Update counters in the status summary
            document.getElementById('answeredCount').textContent = answeredCount;
            document.getElementById('notAnsweredCount').textContent = notAnsweredCount;
            document.getElementById('reviewCount').textContent = reviewCount;
            document.getElementById('bookmarkedCount').textContent = bookmarkedCount;
        }}
        function toggleBookmark() {{
            if (bookmarkedQuestions.has(currentQuestionIndex)) {{
                bookmarkedQuestions.delete(currentQuestionIndex);
            }} else {{
                bookmarkedQuestions.add(currentQuestionIndex);
            }}
            displayQuestion(currentQuestionIndex);
            updatePalette();
        }}

        function clearSelection() {{
            userAnswers[currentQuestionIndex] = null;
            displayQuestion(currentQuestionIndex);
            updatePalette();
        }}

        function markAsReview() {{
            if (!reviewedQuestions) {{
                reviewedQuestions = new Set();
            }}
            
            if (reviewedQuestions.has(currentQuestionIndex)) {{
                reviewedQuestions.delete(currentQuestionIndex);
            }} else {{
                reviewedQuestions.add(currentQuestionIndex);
            }}
            
            displayQuestion(currentQuestionIndex);
            updatePalette();
        }}

        // Add double-click functionality to uncheck answers
        document.addEventListener('click', (e) => {{
            const option = e.target.closest('.option');
            if (option) {{
                if (e.detail === 2) {{ // Check if it's a double click
                    clearSelection();
                }}
            }}
            
            const palette = document.getElementById('questionPalette');
            const paletteToggle = document.querySelector('.palette-toggle');
            
            if (window.innerWidth <= 768 && 
                !palette.contains(e.target) && 
                !paletteToggle.contains(e.target) &&
                palette.style.display === 'block') {{
                palette.style.display = 'none';
            }}
        }});

        // Initialize
        startTimer();
        displayQuestion(0);

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {{
            // Prevent default behavior for arrow keys to avoid scrolling
            if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {{
                e.preventDefault();
            }}
            
            // Handle navigation and shortcuts
            switch (e.key) {{
                case 'ArrowRight':
                case 'n':
                    nextQuestion();
                    break;
                case 'ArrowLeft':
                case 'p':
                    previousQuestion();
                    break;
                case '1':
                case '2':
                case '3':
                case '4':
                    selectOption(parseInt(e.key));
                    break;
                case 'b':
                    toggleBookmark();
                    break;
                case ' ':
                    e.preventDefault();
                    togglePalette();
                    break;
            }}
        }});

        // Add keyboard shortcut help
        function showKeyboardShortcuts() {{
            alert(`
Keyboard Shortcuts:
- Arrow Right or 'N': Next question
- Arrow Left or 'P': Previous question
- 1-4: Select answer option
- 'B': Bookmark/Unbookmark current question
- 'Space': Toggle question palette
            `.trim());
        }}

        function filterReviewItems(status) {{
            // Update active state of filter buttons
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
                if (btn.onclick.toString().includes(`'${{status}}'`)) {{
                    btn.classList.add('active');
                }}
            }});
            
            // Show/hide review items based on status
            const reviewItems = document.querySelectorAll('.review-item');
            let visibleCount = 0;
            
            reviewItems.forEach(item => {{
                if (status === 'all' || item.dataset.status === status) {{
                    item.style.display = 'block';
                    visibleCount++;
                }} else {{
                    item.style.display = 'none';
                }}
            }});

            // Show "no items" message if no items are visible
            const noItemsMessage = document.getElementById('noItemsMessage') || (() => {{
                const msg = document.createElement('div');
                msg.id = 'noItemsMessage';
                msg.className = 'no-items-message';
                document.querySelector('.question-review').appendChild(msg);
                return msg;
            }})();

            if (visibleCount === 0) {{
                noItemsMessage.style.display = 'block';
                noItemsMessage.textContent = `No ${{status === 'all' ? '' : status}} questions found`;
            }} else {{
                noItemsMessage.style.display = 'none';
            }}
        }}

        // Clean up all intervals when page is unloaded
        window.addEventListener('beforeunload', () => {{
            clearInterval(timerInterval);
            if (window.questionTimerInterval) {{
                clearInterval(window.questionTimerInterval);
            }}
        }});
    </script>
</body>
</html>
"""
    FileName = FileName.replace('/', '-').replace('|', ' ') + ".html"
    with open(FileName, "w", encoding="utf-8") as f:
        f.write(html)
    return FileName


async def make_APPX_quiz_HTML(name: str, data):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{name}</title>
<style>
:root {{--primary-color: #007bff; --primary-hover: #0069d9; --success-color: #28a745; --success-hover: #218838; --danger-color: #dc3545; --warning-color: #ffc107; --secondary-color: #6c757d; --bg-primary: #ffffff; --bg-secondary: #f8f9fa; --bg-tertiary: #e9ecef; --text-primary: #212529; --text-secondary: #6c757d; --border-color: #dee2e6; --shadow: 0 4px 6px rgba(0,0,0,0.1); --shadow-lg: 0 10px 30px rgba(0,0,0,0.15); --overlay: rgba(0,0,0,0.5); --nav-height: 80px;}}

[data-theme="dark"] {{--primary-color: #4dabf7; --primary-hover: #339af0; --success-color: #51cf66; --success-hover: #40c057; --danger-color: #ff6b6b; --warning-color: #ffd43b; --secondary-color: #868e96; --bg-primary: #1a1a1a; --bg-secondary: #2d2d2d; --bg-tertiary: #404040; --text-primary: #f8f9fa; --text-secondary: #adb5bd; --border-color: #495057; --shadow: 0 4px 6px rgba(0,0,0,0.3); --shadow-lg: 0 10px 30px rgba(0,0,0,0.4); --overlay: rgba(0,0,0,0.7);}}

* {{box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; touch-action: manipulation;}}
html {{-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; scroll-behavior: smooth;}}

body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg-secondary); color: var(--text-primary); line-height: 1.6; transition: background 0.3s, color 0.3s; overflow-x: hidden; position: relative; padding-bottom: var(--nav-height);}}
body.palette-open {{overflow: hidden; position: fixed; width: 100%;}}

.container {{max-width: 1200px; margin: 0 auto; padding: 20px;}}

.header {{display: flex; justify-content: space-between; align-items: center; background: var(--bg-primary); padding: 20px 30px; border-radius: 15px; margin-bottom: 20px; box-shadow: var(--shadow);}}

.header h1 {{font-size: 28px; color: var(--primary-color); font-weight: 700; user-select: none;}}
.header-controls {{display: flex; gap: 15px; align-items: center;}}

.theme-toggle, .fullscreen-btn {{background: var(--bg-tertiary); border: none; padding: 10px 15px; border-radius: 8px; cursor: pointer; font-size: 20px; transition: all 0.3s; min-width: 44px; min-height: 44px; user-select: none;}}
.theme-toggle:active, .fullscreen-btn:active {{transform: scale(0.95);}}
.theme-toggle:hover, .fullscreen-btn:hover {{background: var(--primary-color); color: white;}}

.timer {{background: var(--warning-color); color: #000; padding: 10px 20px; border-radius: 8px; font-weight: 600; font-size: 18px; min-width: 100px; text-align: center; user-select: none;}}
.timer.warning {{animation: pulse 1s infinite;}}

@keyframes pulse {{0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }}}}

.palette-fab {{
  position: fixed;
  bottom: calc(var(--nav-height) + 20px);
  right: 20px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--primary-color);
  color: white;
  border: none;
  cursor: pointer;
  font-size: 24px;
  box-shadow: 0 6px 20px rgba(0,123,255,0.4);
  transition: all 0.3s ease;
  z-index: 998;
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
  touch-action: manipulation;
}}

.palette-fab:active {{
  transform: scale(0.9);
}}

.palette-fab:hover {{
  transform: scale(1.05);
  box-shadow: 0 8px 25px rgba(0,123,255,0.6);
}}

.palette-fab.active {{
  background: var(--danger-color);
}}

.palette-fab .badge {{
  position: absolute;
  top: -5px;
  right: -5px;
  background: var(--success-color);
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--bg-secondary);
  pointer-events: none;
}}

.palette-overlay {{
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--overlay);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 999;
  touch-action: none;
}}

.palette-overlay.active {{
  opacity: 1;
  visibility: visible;
}}

.question-palette {{
  position: fixed;
  top: 0;
  right: -100%;
  width: 100%;
  max-width: 450px;
  height: 100vh;
  height: 100dvh;
  background: var(--bg-primary);
  box-shadow: -5px 0 20px rgba(0,0,0,0.2);
  transition: right 0.3s ease;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}}

.question-palette.active {{
  right: 0;
}}

.palette-header {{
  padding: 20px;
  background: var(--primary-color);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
  user-select: none;
}}

.palette-header h3 {{
  font-size: 20px;
  margin: 0;
}}

.palette-close {{
  background: transparent;
  border: none;
  color: white;
  font-size: 32px;
  cursor: pointer;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: background 0.2s;
  line-height: 1;
  touch-action: manipulation;
}}

.palette-close:active {{
  transform: scale(0.9);
}}

.palette-close:hover {{
  background: rgba(255,255,255,0.2);
}}

.palette-stats {{
  padding: 15px 20px;
  background: var(--bg-tertiary);
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  font-size: 13px;
  text-align: center;
  flex-shrink: 0;
  border-bottom: 1px solid var(--border-color);
  user-select: none;
}}

.palette-stat {{
  display: flex;
  flex-direction: column;
}}

.palette-stat .number {{
  font-size: 24px;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 5px;
}}

.palette-stat.answered .number {{ color: var(--success-color); }}
.palette-stat.unanswered .number {{ color: var(--secondary-color); }}
.palette-stat.bookmarked .number {{ color: var(--warning-color); }}

.palette-search {{
  padding: 15px 20px;
  background: var(--bg-secondary);
  flex-shrink: 0;
}}

.palette-search input {{
  width: 100%;
  padding: 10px 15px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 14px;
  -webkit-appearance: none;
  appearance: none;
}}

.palette-search input:focus {{
  outline: none;
  border-color: var(--primary-color);
}}

.palette-content {{
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 20px;
  -webkit-overflow-scrolling: touch;
}}

.palette-grid {{
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 10px;
}}

.palette-btn {{
  aspect-ratio: 1;
  border: 2px solid var(--border-color);
  background: var(--bg-secondary);
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
  min-width: 40px;
  min-height: 40px;
  color: var(--text-primary);
  position: relative;
  user-select: none;
  touch-action: manipulation;
}}

.palette-btn:active {{
  transform: scale(0.9);
}}

.palette-btn:hover {{
  transform: scale(1.1);
  z-index: 10;
  box-shadow: var(--shadow);
}}

.palette-btn.current {{
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  animation: currentPulse 2s infinite;
}}

@keyframes currentPulse {{
  0%, 100% {{ box-shadow: 0 0 0 0 rgba(0,123,255,0.7); }}
  50% {{ box-shadow: 0 0 0 8px rgba(0,123,255,0); }}
}}

.palette-btn.answered {{
  background: var(--success-color);
  color: white;
  border-color: var(--success-color);
}}

.palette-btn.bookmarked::after {{
  content: '🔖';
  position: absolute;
  top: -8px;
  right: -8px;
  font-size: 16px;
  pointer-events: none;
}}

.palette-btn.bookmarked.answered {{
  background: var(--success-color);
}}

.palette-legend {{
  padding: 20px;
  border-top: 1px solid var(--border-color);
  font-size: 13px;
  background: var(--bg-secondary);
  flex-shrink: 0;
  user-select: none;
}}

.legend-grid {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}}

.legend-item {{
  display: flex;
  align-items: center;
  gap: 10px;
}}

.legend-color {{
  width: 24px;
  height: 24px;
  border-radius: 6px;
  flex-shrink: 0;
}}

.quiz-container {{
  background: var(--bg-primary);
  border-radius: 15px;
  box-shadow: var(--shadow-lg);
  padding: 30px;
  max-width: 900px;
  margin: 0 auto;
  scroll-margin-top: 20px;
}}

.quiz-header {{
  text-align: center;
  margin-bottom: 20px;
}}

.marking-info {{
  display: inline-block;
  background: var(--bg-tertiary);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  color: var(--text-secondary);
  user-select: none;
}}

.progress-section {{
  margin-bottom: 25px;
}}

.progress-stats {{
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
  color: var(--text-secondary);
  user-select: none;
}}

.progress-bar-container {{
  background: var(--bg-tertiary);
  border-radius: 12px;
  overflow: hidden;
  height: 10px;
}}

.progress-bar {{
  height: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--success-color));
  transition: width 0.4s ease;
  border-radius: 12px;
}}

.question-section {{
  min-height: 300px;
  scroll-margin-top: 80px;
  margin-bottom: 20px;
}}

.question-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}}

.question-number {{
  font-size: 14px;
  font-weight: 600;
  color: var(--primary-color);
  user-select: none;
}}

.bookmark-btn {{
  background: transparent;
  border: 2px solid var(--border-color);
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 44px;
  min-height: 44px;
  user-select: none;
  touch-action: manipulation;
}}

.bookmark-btn:active {{
  transform: scale(0.95);
}}

.bookmark-btn.active {{
  background: var(--warning-color);
  border-color: var(--warning-color);
  color: #000;
}}

.question {{
  font-size: 18px;
  line-height: 1.7;
  margin-bottom: 25px;
  color: var(--text-primary);
  user-select: text;
}}

.question-image {{
  max-width: 100%;
  max-height: 400px;
  border-radius: 10px;
  object-fit: contain;
  background: var(--bg-primary);
  padding: 10px;
}}

.options {{
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}}

.option-label {{
  display: flex;
  align-items: center;
  border: 2px solid var(--border-color);
  padding: 16px 20px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  background: var(--bg-secondary);
  min-height: 60px;
  user-select: none;
  touch-action: manipulation;
}}

.option-label:active {{
  transform: scale(0.98);
}}

.option-label:hover {{
  background: var(--bg-tertiary);
  border-color: var(--primary-color);
}}

.option-label.selected {{
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}}

.option-label input[type="radio"] {{
  margin-right: 15px;
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: var(--primary-color);
  flex-shrink: 0;
}}

.option-content {{
  flex: 1;
  display: flex;
  align-items: center;
}}

.option-image {{
  max-width: 100%;
  max-height: 200px;
  border-radius: 8px;
  object-fit: contain;
  background: var(--bg-primary);
  padding: 10px;
}}

.option-label.selected .option-image {{
  background: rgba(255,255,255,0.1);
}}

/* FIXED NAVIGATION - KEY UPDATE */
.navigation {{
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--bg-primary);
  border-top: 2px solid var(--border-color);
  box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
  z-index: 997;
  padding: 15px 20px;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 10px;
  max-width: 100%;
}}

.nav-btn {{
  padding: 14px 20px;
  border-radius: 10px;
  border: none;
  font-size: 16px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  min-height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  user-select: none;
  touch-action: manipulation;
  white-space: nowrap;
}}

.nav-btn:active {{
  transform: scale(0.97);
}}

.nav-btn:disabled {{
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}}

.nav-btn.prev {{
  background: var(--secondary-color);
  color: white;
}}

.nav-btn.prev:hover:not(:disabled) {{
  background: #5a6268;
}}

.nav-btn.next {{
  background: var(--primary-color);
  color: white;
}}

.nav-btn.next:hover:not(:disabled) {{
  background: var(--primary-hover);
}}

.nav-btn.clear {{
  background: var(--danger-color);
  color: white;
}}

.nav-btn.clear:hover {{
  background: #c82333;
}}

.nav-btn.submit {{
  background: var(--success-color);
  color: white;
  grid-column: 1 / -1;
}}

.nav-btn.submit:hover {{
  background: var(--success-hover);
}}

.result-section {{
  animation: fadeIn 0.5s;
}}

@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(20px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

.score-card {{
  background: linear-gradient(135deg, var(--primary-color), var(--success-color));
  color: white;
  padding: 30px;
  border-radius: 15px;
  text-align: center;
  margin-bottom: 30px;
  user-select: none;
}}

.score-card h2 {{
  font-size: 48px;
  margin-bottom: 10px;
}}

.score-card p {{
  font-size: 18px;
  opacity: 0.9;
}}

.stats-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}}

.stat-card {{
  background: var(--bg-secondary);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  border: 2px solid var(--border-color);
  user-select: none;
}}

.stat-card h3 {{
  font-size: 32px;
  margin-bottom: 8px;
}}

.stat-card.correct h3 {{ color: var(--success-color); }}
.stat-card.wrong h3 {{ color: var(--danger-color); }}
.stat-card.unattempted h3 {{ color: var(--secondary-color); }}

.question-review {{
  border: 2px solid var(--border-color);
  border-radius: 15px;
  padding: 25px;
  margin-bottom: 20px;
  background: var(--bg-secondary);
}}

.question-review h4 {{
  margin-bottom: 15px;
  font-size: 16px;
  line-height: 1.6;
}}

.review-option {{
  padding: 12px 16px;
  border-radius: 10px;
  margin-bottom: 10px;
  border: 2px solid var(--border-color);
  background: var(--bg-primary);
  user-select: none;
  display: flex;
  align-items: center;
  gap: 10px;
}}

.review-option .option-image {{
  max-width: 150px;
  max-height: 100px;
}}

.review-option.correct {{
  background: #d4edda;
  border-color: var(--success-color);
  color: #155724;
}}

.review-option.wrong {{
  background: #f8d7da;
  border-color: var(--danger-color);
  color: #721c24;
}}

.review-option.user-selected {{
  border-width: 3px;
  font-weight: 600;
}}

.action-buttons {{
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 20px;
}}

.action-btn {{
  padding: 14px 30px;
  border-radius: 10px;
  border: none;
  font-size: 16px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  min-width: 150px;
  user-select: none;
  touch-action: manipulation;
}}

.action-btn:active {{
  transform: scale(0.95);
}}

.action-btn.restart {{
  background: var(--danger-color);
  color: white;
}}

.action-btn.restart:hover {{
  background: #c82333;
}}

.action-btn.download {{
  background: var(--primary-color);
  color: white;
}}

.action-btn.download:hover {{
  background: var(--primary-hover);
}}

.action-btn.print {{
  background: var(--secondary-color);
  color: white;
}}

.action-btn.print:hover {{
  background: #5a6268;
}}

.hidden {{
  display: none !important;
}}

.palette-content::-webkit-scrollbar {{
  width: 8px;
}}

.palette-content::-webkit-scrollbar-track {{
  background: var(--bg-tertiary);
}}

.palette-content::-webkit-scrollbar-thumb {{
  background: var(--primary-color);
  border-radius: 4px;
}}

.palette-content::-webkit-scrollbar-thumb:hover {{
  background: var(--primary-hover);
}}

@media (max-width: 768px) {{
  :root {{
    --nav-height: 140px;
  }}

  .container {{
    padding: 10px;
  }}

  .header {{
    flex-direction: column;
    gap: 15px;
    padding: 15px;
  }}

  .header h1 {{
    font-size: 22px;
  }}

  .quiz-container {{
    padding: 20px 15px;
  }}

  .question-palette {{
    width: 100%;
    max-width: 100%;
  }}

  .palette-grid {{
    grid-template-columns: repeat(6, 1fr);
    gap: 8px;
  }}

  .palette-btn {{
    font-size: 13px;
    min-width: 36px;
    min-height: 36px;
  }}

  .palette-fab {{
    bottom: calc(var(--nav-height) + 10px);
    right: 15px;
    width: 56px;
    height: 56px;
    font-size: 22px;
  }}

  .navigation {{
    grid-template-columns: 1fr;
    gap: 10px;
    padding: 12px 15px;
  }}

  .nav-btn {{
    min-height: 44px;
    font-size: 15px;
  }}

  .nav-btn.clear {{
    order: 3;
  }}

  .nav-btn.submit {{
    grid-column: auto;
  }}

  .stats-grid {{
    grid-template-columns: repeat(2, 1fr);
  }}

  .legend-grid {{
    grid-template-columns: 1fr;
  }}

  .question {{
    font-size: 16px;
  }}

  .option-label {{
    padding: 14px 16px;
    font-size: 15px;
  }}

  .option-image {{
    max-height: 150px;
  }}

  .action-buttons {{
    flex-direction: column;
  }}

  .action-btn {{
    width: 100%;
  }}
}}

@media (max-width: 480px) {{
  .palette-grid {{
    grid-template-columns: repeat(5, 1fr);
    gap: 6px;
  }}

  .palette-btn {{
    font-size: 12px;
    min-width: 32px;
    min-height: 32px;
  }}

  .header h1 {{
    font-size: 20px;
  }}

  .timer {{
    font-size: 16px;
    padding: 8px 16px;
  }}

  .option-image {{
    max-height: 120px;
  }}
}}

@media (max-width: 360px) {{
  .palette-grid {{
    grid-template-columns: repeat(4, 1fr);
  }}
}}

@media print {{
  .header-controls, .navigation, .palette-fab, .palette-overlay, .question-palette, .action-buttons, .bookmark-btn {{
    display: none !important;
  }}

  body {{
    background: white;
    padding-bottom: 0;
  }}

  .container {{
    padding-bottom: 20px;
  }}
}}

@media (max-height: 500px) and (orientation: landscape) {{
  .palette-fab {{
    bottom: calc(var(--nav-height) + 5px);
    right: 10px;
    width: 48px;
    height: 48px;
    font-size: 20px;
  }}

  .palette-fab .badge {{
    width: 20px;
    height: 20px;
    font-size: 11px;
  }}
}}
</style>
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['\\(', '\\)'], ['$', '$']] }},
  svg: {{ fontCache: 'global' }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>


</head>
<body>
<div class="container">
  <div class="header">
    <h1>{name}</h1>
    <div class="header-controls">
      <div class="timer" id="timer">00:00</div>
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode" title="Toggle Theme">🌙</button>
      <button class="fullscreen-btn" id="fullscreenBtn" aria-label="Toggle fullscreen" title="Fullscreen">⛶</button>
    </div>
  </div>

  <div class="quiz-container" id="quizContainer">
    <div class="quiz-header">
      <div class="marking-info" id="markingInfo">Marking: +1, -0</div>
    </div>

    <div class="progress-section">
      <div class="progress-stats">
        <span>Progress: <strong id="progressText">1/2</strong></span>
        <span>Attempted: <strong id="attemptedText">0</strong></span>
      </div>
      <div class="progress-bar-container">
        <div class="progress-bar" id="progressBar"></div>
      </div>
    </div>

    <div class="question-section" id="questionSection">
      <div class="question-header">
        <div class="question-number" id="questionNumber">Question 1 of 2</div>
        <button class="bookmark-btn" id="bookmarkBtn" aria-label="Bookmark question">
          <span>🔖</span> <span>Bookmark</span>
        </button>
      </div>
      
      <div class="question" id="questionText"></div>
      
      <div class="options" id="optionsContainer"></div>
    </div>

    <div class="result-section hidden" id="resultSection"></div>
  </div>
</div>

<!-- FIXED NAVIGATION BAR -->
<div class="navigation" id="navigation">
  <button class="nav-btn prev" id="prevBtn" aria-label="Previous question">
    <span>←</span> Previous
  </button>
  <button class="nav-btn clear" id="clearBtn" aria-label="Clear answer">
    Clear
  </button>
  <button class="nav-btn next" id="nextBtn" aria-label="Next question">
    Next <span>→</span>
  </button>
  <button class="nav-btn submit hidden" id="submitBtn" aria-label="Submit quiz">
    Submit Quiz
  </button>
</div>

<button class="palette-fab" id="paletteFab" aria-label="Toggle question palette" title="Question Palette (P)">
  📋
  <span class="badge" id="answeredBadge">0</span>
</button>

<div class="palette-overlay" id="paletteOverlay"></div>

<div class="question-palette" id="questionPalette">
  <div class="palette-header">
    <h3>Question Palette</h3>
    <button class="palette-close" id="paletteClose" aria-label="Close palette">×</button>
  </div>

  <div class="palette-stats">
    <div class="palette-stat answered">
      <div class="number" id="paletteAnswered">0</div>
      <div>Answered</div>
    </div>
    <div class="palette-stat unanswered">
      <div class="number" id="paletteUnanswered">2</div>
      <div>Not Answered</div>
    </div>
    <div class="palette-stat bookmarked">
      <div class="number" id="paletteBookmarked">0</div>
      <div>Bookmarked</div>
    </div>
  </div>

  <div class="palette-search">
    <input type="number" id="paletteSearch" placeholder="Jump to question number..." aria-label="Search questions" inputmode="numeric" pattern="[0-9]*">
  </div>

  <div class="palette-content">
    <div class="palette-grid" id="paletteGrid"></div>
  </div>

  <div class="palette-legend">
    <div class="legend-grid">
      <div class="legend-item">
        <div class="legend-color" style="background: var(--success-color);"></div>
        <span>Answered</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background: var(--bg-secondary); border: 2px solid var(--border-color);"></div>
        <span>Not Answered</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background: var(--primary-color);"></div>
        <span>Current Question</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background: var(--warning-color);"></div>
        <span>🔖 Bookmarked</span>
      </div>
    </div>
  </div>
</div>

<script>
const questions = {data};

let currentQuestion = 0;
let answers = {{}};
let bookmarks = new Set();
let timerSeconds = 0;
let timerInterval = null;
let isPaletteOpen = false;

// Use a namespaced storage key so different quizzes/pages don't collide
const STORAGE_KEY = 'quizState_' + (document.title || 'default');

function isImageURL(str) {{
  return str && (str.startsWith('http://') || str.startsWith('https://'));
}}

function createOptionContent(optionText) {{
  const contentDiv = document.createElement('div');
  contentDiv.className = 'option-content';
  
  if (isImageURL(optionText)) {{
    const img = document.createElement('img');
    img.src = optionText;
    img.className = 'option-image';
    img.alt = 'Option image';
    img.loading = 'lazy';
    img.onerror = function() {{
      this.style.display = 'none';
      const errorText = document.createTextNode('Image failed to load');
      contentDiv.appendChild(errorText);
    }};
    contentDiv.appendChild(img);
  }} else {{
    const text = document.createTextNode(optionText);
    contentDiv.appendChild(text);
  }}
  
  return contentDiv;
}}

document.addEventListener('DOMContentLoaded', () => {{
  initTheme();
  initQuiz();
  initEventListeners();
  loadFromLocalStorage();
  startTimer();
  createPalette();
  preventDoubleTapZoom();
}});

function preventDoubleTapZoom() {{
  let lastTouchEnd = 0;
  document.addEventListener('touchend', (event) => {{
    const now = Date.now();
    if (now - lastTouchEnd <= 300) {{
      event.preventDefault();
    }}
    lastTouchEnd = now;
  }}, {{ passive: false }});
}}

function initTheme() {{
  const savedTheme = localStorage.getItem('quizTheme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon();
}}

function updateThemeIcon() {{
  const theme = document.documentElement.getAttribute('data-theme');
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {{
    themeBtn.textContent = theme === 'dark' ? '☀️' : '🌙';
  }}
}}

function toggleTheme() {{
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('quizTheme', newTheme);
  updateThemeIcon();
}}

function initQuiz() {{
  loadQuestion(currentQuestion);
  updateMarkingInfo();
}}

function initEventListeners() {{
  const themeBtn = document.getElementById('themeToggle');
  const fullscreenBtn = document.getElementById('fullscreenBtn');
  
  if (themeBtn) {{
    themeBtn.addEventListener('click', toggleTheme);
    themeBtn.addEventListener('touchend', (e) => {{
      e.preventDefault();
      toggleTheme();
    }});
  }}
  
  if (fullscreenBtn) {{
    fullscreenBtn.addEventListener('click', toggleFullscreen);
    fullscreenBtn.addEventListener('touchend', (e) => {{
      e.preventDefault();
      toggleFullscreen();
    }});
  }}
  
  addButtonListener('prevBtn', prevQuestion);
  addButtonListener('nextBtn', nextQuestion);
  addButtonListener('clearBtn', clearAnswer);
  addButtonListener('submitBtn', confirmSubmit);
  addButtonListener('bookmarkBtn', toggleBookmark);
  
  addButtonListener('paletteFab', togglePalette);
  addButtonListener('paletteClose', closePalette);
  
  const overlay = document.getElementById('paletteOverlay');
  if (overlay) {{
    overlay.addEventListener('click', closePalette);
    overlay.addEventListener('touchend', (e) => {{
      e.preventDefault();
      closePalette();
    }});
  }}
  
  const searchInput = document.getElementById('paletteSearch');
  if (searchInput) {{
    searchInput.addEventListener('input', handleSearch);
    searchInput.addEventListener('change', jumpToQuestion);
  }}
  
  document.addEventListener('keydown', handleKeyPress);
  
  setInterval(saveToLocalStorage, 5000);
  
  document.addEventListener('visibilitychange', () => {{
    if (!document.hidden) {{
      updatePalette();
    }}
  }});
}}

function addButtonListener(id, handler) {{
  const btn = document.getElementById(id);
  if (btn) {{
    btn.addEventListener('click', handler);
    btn.addEventListener('touchend', (e) => {{
      e.preventDefault();
      handler();
    }});
  }}
}}

function jumpToQuestion(e) {{
  const questionNum = parseInt(e.target.value);
  if (questionNum >= 1 && questionNum <= questions.length) {{
    goToQuestion(questionNum - 1);
    closePalette();
    e.target.value = '';
  }}
}}

function togglePalette() {{
  isPaletteOpen = !isPaletteOpen;
  const palette = document.getElementById('questionPalette');
  const overlay = document.getElementById('paletteOverlay');
  const fab = document.getElementById('paletteFab');
  
  if (isPaletteOpen) {{
    palette.classList.add('active');
    overlay.classList.add('active');
    fab.classList.add('active');
    fab.innerHTML = '✕<span class="badge" id="answeredBadge">' + Object.keys(answers).length + '</span>';
    document.body.classList.add('palette-open');
  }} else {{
    closePalette();
  }}
}}

function closePalette() {{
  isPaletteOpen = false;
  const palette = document.getElementById('questionPalette');
  const overlay = document.getElementById('paletteOverlay');
  const fab = document.getElementById('paletteFab');
  
  if (palette) palette.classList.remove('active');
  if (overlay) overlay.classList.remove('active');
  if (fab) {{
    fab.classList.remove('active');
    fab.innerHTML = '📋<span class="badge" id="answeredBadge">' + Object.keys(answers).length + '</span>';
  }}
  document.body.classList.remove('palette-open');
}}

function handleSearch(e) {{
  const searchTerm = e.target.value.toLowerCase();
  if (!searchTerm) {{
    document.querySelectorAll('.palette-btn').forEach(btn => {{
      btn.style.display = '';
    }});
    return;
  }}
  
  const buttons = document.querySelectorAll('.palette-btn');
  buttons.forEach((btn, index) => {{
    const questionNum = (index + 1).toString();
    if (questionNum.includes(searchTerm)) {{
      btn.style.display = '';
    }} else {{
      btn.style.display = 'none';
    }}
  }});
}}

function handleKeyPress(e) {{
  if (document.getElementById('resultSection').classList.contains('hidden')) {{
    if (e.key === 'Escape' && isPaletteOpen) {{
      closePalette();
    }} else if (!isPaletteOpen && e.target.tagName !== 'INPUT') {{
      if (e.key === 'ArrowLeft') {{
        e.preventDefault();
        prevQuestion();
      }} else if (e.key === 'ArrowRight') {{
        e.preventDefault();
        nextQuestion();
      }} else if (e.key === 'Enter') {{
        e.preventDefault();
        nextQuestion();
      }} else if (e.key === 'b' || e.key === 'B') {{
        e.preventDefault();
        toggleBookmark();
      }} else if (e.key === 'c' || e.key === 'C') {{
        e.preventDefault();
        clearAnswer();
      }} else if (e.key === 'p' || e.key === 'P') {{
        e.preventDefault();
        togglePalette();
      }} else if (e.key >= '1' && e.key <= '4') {{
        e.preventDefault();
        selectOption(parseInt(e.key));
      }}
    }}
  }}
}}

function selectOption(optionNum) {{
  const q = questions[currentQuestion];
  const radio = document.querySelector(`input[name="q${{q.sr_no}}"][value="${{optionNum}}"]`);
  if (radio) {{
    radio.checked = true;
    const label = radio.closest('.option-label');
    if (label) {{
      document.querySelectorAll('.option-label').forEach(l => l.classList.remove('selected'));
      label.classList.add('selected');
      saveAnswer();
    }}
  }}
}}

function toggleFullscreen() {{
  try {{
    if (!document.fullscreenElement) {{
      document.documentElement.requestFullscreen().catch(err => {{
        console.log('Fullscreen error:', err);
      }});
    }} else {{
      document.exitFullscreen();
    }}
  }} catch (err) {{
    console.log('Fullscreen not supported');
  }}
}}

function startTimer() {{
  if (timerInterval) {{
    clearInterval(timerInterval);
  }}
  timerInterval = setInterval(() => {{
    timerSeconds++;
    updateTimer();
    if (timerSeconds > 600) {{
      const timer = document.getElementById('timer');
      if (timer) timer.classList.add('warning');
    }}
  }}, 1000);
}}

function updateTimer() {{
  const minutes = Math.floor(timerSeconds / 60);
  const seconds = timerSeconds % 60;
  const timer = document.getElementById('timer');
  if (timer) {{
    timer.textContent = 
      `${{minutes.toString().padStart(2, '0')}}:${{seconds.toString().padStart(2, '0')}}`;
  }}
}}

function createPalette() {{
  const grid = document.getElementById('paletteGrid');
  if (!grid) return;
  
  grid.innerHTML = '';
  questions.forEach((q, index) => {{
    const btn = document.createElement('button');
    btn.textContent = index + 1;
    btn.className = 'palette-btn';
    btn.setAttribute('aria-label', `Go to question ${{index + 1}}`);
    btn.setAttribute('type', 'button');
    
    btn.addEventListener('click', () => {{
      goToQuestion(index);
      closePalette();
    }});
    
    btn.addEventListener('touchend', (e) => {{
      e.preventDefault();
      goToQuestion(index);
      closePalette();
    }});
    
    grid.appendChild(btn);
  }});
  updatePalette();
}}

function updatePalette() {{
  const buttons = document.querySelectorAll('.palette-btn');
  buttons.forEach((btn, index) => {{
    btn.className = 'palette-btn';
    if (index === currentQuestion) btn.classList.add('current');
    if (answers[questions[index].sr_no]) btn.classList.add('answered');
    if (bookmarks.has(questions[index].sr_no)) btn.classList.add('bookmarked');
  }});
  
  updatePaletteStats();
}}

function updatePaletteStats() {{
  const answered = Object.keys(answers).length;
  const unanswered = questions.length - answered;
  const bookmarkedCount = bookmarks.size;
  
  const answeredEl = document.getElementById('paletteAnswered');
  const unansweredEl = document.getElementById('paletteUnanswered');
  const bookmarkedEl = document.getElementById('paletteBookmarked');
  
  if (answeredEl) answeredEl.textContent = answered;
  if (unansweredEl) unansweredEl.textContent = unanswered;
  if (bookmarkedEl) bookmarkedEl.textContent = bookmarkedCount;
  
  const badge = document.querySelector('.palette-fab .badge');
  if (badge) badge.textContent = answered;
}}

function goToQuestion(index) {{
  if (index < 0 || index >= questions.length) return;
  saveAnswer();
  currentQuestion = index;
  loadQuestion(currentQuestion);
  
  const questionSection = document.getElementById('questionSection');
  if (questionSection) {{
    setTimeout(() => {{
      questionSection.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}, 100);
  }}
}}

function loadQuestion(index) {{
  const q = questions[index];
  
  const questionNumber = document.getElementById('questionNumber');
  const questionText = document.getElementById('questionText');
  
  if (questionNumber) {{
    questionNumber.textContent = `Question ${{index + 1}} of ${{questions.length}}`;
  }}
  
  if (questionText) {{
    // Render question as image if it's a URL, otherwise as text
    questionText.innerHTML = '';
    if (isImageURL(q.question)) {{
      const img = document.createElement('img');
      img.src = q.question;
      img.className = 'question-image';
      img.alt = 'Question image';
      img.loading = 'lazy';
      img.onerror = function() {{
        this.style.display = 'none';
        questionText.textContent = q.question;
      }};
      questionText.appendChild(img);
    }} else {{
      questionText.textContent = q.question;
    }}
  }}
  
  const container = document.getElementById('optionsContainer');
  if (!container) return;
  
  container.innerHTML = '';
  
  for (let i = 1; i <= 4; i++) {{
    const label = document.createElement('label');
    label.className = 'option-label';
    if (answers[q.sr_no] == i) label.classList.add('selected');
    
    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.name = `q${{q.sr_no}}`;
    radio.value = i;
    radio.checked = answers[q.sr_no] == i;
    
    const changeHandler = () => {{
      document.querySelectorAll('.option-label').forEach(l => l.classList.remove('selected'));
      label.classList.add('selected');
      saveAnswer();
    }};
    
    radio.addEventListener('change', changeHandler);
    label.addEventListener('click', (e) => {{
      if (e.target !== radio) {{
        radio.checked = true;
        changeHandler();
      }}
    }});
    
    label.appendChild(radio);
    
    const optionContent = createOptionContent(q[`option${{i}}`]);
    label.appendChild(optionContent);
    
    container.appendChild(label);
  }}
  
  const bookmarkBtn = document.getElementById('bookmarkBtn');
  if (bookmarkBtn) {{
    if (bookmarks.has(q.sr_no)) {{
      bookmarkBtn.classList.add('active');
    }} else {{
      bookmarkBtn.classList.remove('active');
    }}
  }}
  
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const submitBtn = document.getElementById('submitBtn');
  
  if (prevBtn) prevBtn.disabled = index === 0;
  
  if (index === questions.length - 1) {{
    if (nextBtn) nextBtn.classList.add('hidden');
    if (submitBtn) submitBtn.classList.remove('hidden');
  }} else {{
    if (nextBtn) nextBtn.classList.remove('hidden');
    if (submitBtn) submitBtn.classList.add('hidden');
  }}
  
  updateProgress();
  updatePalette();
}}

function updateMarkingInfo() {{
  const q = questions[0];
  const markingInfo = document.getElementById('markingInfo');
  if (markingInfo) {{
    markingInfo.textContent = `Marking: +${{q.positive_marking}}, -${{q.negative_marking}}`;
  }}
}}

// UPDATED: Progress bar now shows current question number
function updateProgress() {{
  const attempted = Object.keys(answers).length;
  const currentProgress = ((currentQuestion + 1) / questions.length) * 100;
  
  const progressBar = document.getElementById('progressBar');
  const progressText = document.getElementById('progressText');
  const attemptedText = document.getElementById('attemptedText');
  
  if (progressBar) progressBar.style.width = `${{currentProgress}}%`;
  if (progressText) progressText.textContent = `${{currentQuestion + 1}}/${{questions.length}}`;
  if (attemptedText) attemptedText.textContent = attempted;
}}

function saveAnswer() {{
  const q = questions[currentQuestion];
  const selected = document.querySelector(`input[name="q${{q.sr_no}}"]:checked`);
  
  if (selected) {{
    answers[q.sr_no] = selected.value;
  }}
  
  updateProgress();
  updatePalette();
  saveToLocalStorage();
}}

function clearAnswer() {{
  const q = questions[currentQuestion];
  delete answers[q.sr_no];
  
  const selected = document.querySelector(`input[name="q${{q.sr_no}}"]:checked`);
  if (selected) selected.checked = false;
  
  document.querySelectorAll('.option-label').forEach(l => l.classList.remove('selected'));
  
  updateProgress();
  updatePalette();
  saveToLocalStorage();
}}

function toggleBookmark() {{
  const q = questions[currentQuestion];
  const btn = document.getElementById('bookmarkBtn');
  
  if (bookmarks.has(q.sr_no)) {{
    bookmarks.delete(q.sr_no);
    if (btn) btn.classList.remove('active');
  }} else {{
    bookmarks.add(q.sr_no);
    if (btn) btn.classList.add('active');
  }}
  
  updatePalette();
  saveToLocalStorage();
}}

function nextQuestion() {{
  saveAnswer();
  if (currentQuestion < questions.length - 1) {{
    currentQuestion++;
    loadQuestion(currentQuestion);
  }}
}}

function prevQuestion() {{
  saveAnswer();
  if (currentQuestion > 0) {{
    currentQuestion--;
    loadQuestion(currentQuestion);
  }}
}}

function confirmSubmit() {{
  const unattempted = questions.length - Object.keys(answers).length;
  let message = 'Are you sure you want to submit the quiz?';
  
  if (unattempted > 0) {{
    message += `\n\nYou have ${{unattempted}} unanswered question(s).`;
  }}
  
  if (confirm(message)) {{
    submitQuiz();
  }}
}}

function submitQuiz() {{
  if (timerInterval) {{
    clearInterval(timerInterval);
    timerInterval = null;
  }}
  saveAnswer();
  closePalette();
  
  let correct = 0, wrong = 0, unattempted = 0, score = 0;
  
  questions.forEach(q => {{
    const userAns = answers[q.sr_no];
    const posMark = parseFloat(q.positive_marking) || 0;
    const negMark = parseFloat(q.negative_marking) || 0;
    
    if (!userAns) {{
      unattempted++;
    }} else if (userAns == q.answer) {{
      correct++;
      score += posMark;
    }} else {{
      wrong++;
      score -= negMark;
    }}
  }});
  
  displayResults(correct, wrong, unattempted, score);
  
  const fab = document.getElementById('paletteFab');
  const nav = document.getElementById('navigation');
  if (fab) fab.style.display = 'none';
  if (nav) nav.style.display = 'none';
  
  document.body.style.paddingBottom = '20px';
  
  clearLocalStorage();
}}

function displayResults(correct, wrong, unattempted, score) {{
  const totalQuestions = questions.length;
  const percentage = ((correct / totalQuestions) * 100).toFixed(1);
  const timerEl = document.getElementById('timer');
  const timeText = timerEl ? timerEl.textContent : '00:00';
  
  let html = `
    <div class="score-card">
      <h2>${{score}}/${{totalQuestions}}</h2>
      <p>Your Score: ${{percentage}}%</p>
      <p>Time Taken: ${{timeText}}</p>
    </div>
    
    <div class="stats-grid">
      <div class="stat-card correct">
        <h3>${{correct}}</h3>
        <p>Correct</p>
      </div>
      <div class="stat-card wrong">
        <h3>${{wrong}}</h3>
        <p>Wrong</p>
      </div>
      <div class="stat-card unattempted">
        <h3>${{unattempted}}</h3>
        <p>Unattempted</p>
      </div>
      <div class="stat-card">
        <h3>${{totalQuestions}}</h3>
        <p>Total</p>
      </div>
    </div>
  `;
  
  questions.forEach(q => {{
    const userAns = answers[q.sr_no];
    const questionHeader = isImageURL(q.question)
      ? `<h4>Q${{q.sr_no}}:</h4><img src="${{q.question}}" class="question-image" alt="Question ${{q.sr_no}}">`
      : `<h4>Q${{q.sr_no}}: ${{q.question}}</h4>`;
    html += `<div class="question-review">${{questionHeader}}`;
    
    for (let i = 1; i <= 4; i++) {{
      const isCorrect = i.toString() === q.answer;
      const isUserAnswer = userAns == i.toString();
      
      let className = 'review-option';
      if (isCorrect) className += ' correct';
      if (isUserAnswer && !isCorrect) className += ' wrong';
      if (isUserAnswer) className += ' user-selected';
      
      const optionValue = q[`option${{i}}`];
      
      if (isImageURL(optionValue)) {{
        html += `<div class="${{className}}">
          ${{isCorrect ? '✓ ' : ''}}${{isUserAnswer ? '➤ ' : ''}} 
          <img src="${{optionValue}}" class="option-image" alt="Option ${{i}}">
        </div>`;
      }} else {{
        html += `<div class="${{className}}">
          ${{isCorrect ? '✓ ' : ''}}${{isUserAnswer ? '➤ ' : ''}}${{optionValue}}
        </div>`;
      }}
    }}
    
    html += `</div>`;
  }});
  
  html += `
    <div class="action-buttons">
      <button class="action-btn restart" onclick="restartQuiz()">Restart Quiz</button>
      <button class="action-btn download" onclick="downloadResults()">Download Results</button>
      <button class="action-btn print" onclick="window.print()">Print Results</button>
    </div>
  `;
  
  const resultSection = document.getElementById('resultSection');
  const questionSection = document.getElementById('questionSection');
  const progressSection = document.querySelector('.progress-section');
  
  if (resultSection) {{
    resultSection.innerHTML = html;
    resultSection.classList.remove('hidden');
  }}
  if (questionSection) questionSection.classList.add('hidden');
  if (progressSection) progressSection.classList.add('hidden');
  
  const quizContainer = document.getElementById('quizContainer');
  if (quizContainer) {{
    setTimeout(() => {{
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}, 100);
  }}
}}

function restartQuiz() {{
  if (confirm('Are you sure you want to restart? All progress will be lost.')) {{
    currentQuestion = 0;
    answers = {{}};
    bookmarks.clear();
    timerSeconds = 0;
    
    const resultSection = document.getElementById('resultSection');
    const questionSection = document.getElementById('questionSection');
    const progressSection = document.querySelector('.progress-section');
    const fab = document.getElementById('paletteFab');
    const nav = document.getElementById('navigation');
    
    if (resultSection) {{
      resultSection.classList.add('hidden');
      resultSection.innerHTML = '';
    }}
    if (questionSection) questionSection.classList.remove('hidden');
    if (progressSection) progressSection.classList.remove('hidden');
    if (fab) fab.style.display = 'flex';
    if (nav) nav.style.display = 'grid';
    
    document.body.style.paddingBottom = 'var(--nav-height)';
    
    if (timerInterval) {{
      clearInterval(timerInterval);
    }}
    startTimer();
    
    loadQuestion(currentQuestion);
    createPalette();
  }}
}}

function downloadResults() {{
  const resultSection = document.getElementById('resultSection');
  if (!resultSection) return;
  
  const resultHTML = resultSection.innerHTML;
  const fullHTML = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Quiz Results - {name}</title>
  <style>
    body {{ font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; max-width: 900px; margin: 0 auto; }}
    .score-card {{ background: linear-gradient(135deg, #007bff, #28a745); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 20px; }}
    .score-card h2 {{ font-size: 48px; margin-bottom: 10px; }}
    .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px; }}
    .stat-card {{ background: white; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #ddd; }}
    .stat-card h3 {{ font-size: 32px; margin-bottom: 8px; }}
    .stat-card.correct h3 {{ color: #28a745; }}
    .stat-card.wrong h3 {{ color: #dc3545; }}
    .stat-card.unattempted h3 {{ color: #6c757d; }}
    .question-review {{ background: white; border: 2px solid #ddd; border-radius: 10px; padding: 20px; margin-bottom: 15px; }}
    .question-review h4 {{ margin-bottom: 15px; font-size: 16px; line-height: 1.6; }}
    .review-option {{ padding: 10px 15px; margin: 8px 0; border-radius: 8px; border: 2px solid #ddd; display: flex; align-items: center; gap: 10px; }}
    .option-image {{ max-width: 150px; max-height: 100px; border-radius: 8px; }}
    .review-option.correct {{ background: #d4edda; border-color: #28a745; color: #155724; }}
    .review-option.wrong {{ background: #f8d7da; border-color: #dc3545; color: #721c24; }}
    .review-option.user-selected {{ border-width: 3px; font-weight: bold; }}
    @media print {{ body {{ background: white; }} }}
    @media (max-width: 600px) {{ .stats-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
  </style>
</head>
<body>
  <h1 style="text-align: center; color: #007bff;">{name} - Quiz Results</h1>
  <p style="text-align: center; color: #666; margin-bottom: 30px;">Generated on: ${{new Date().toLocaleString()}}</p>
  ${{resultHTML.replace(/<div class="action-buttons">[\s\S]*?<\/div>/, '')}}
</body>
</html>
  `;
  
  try {{
    const blob = new Blob([fullHTML], {{ type: 'text/html' }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Quiz_Results_${{new Date().getTime()}}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }} catch (err) {{
    alert('Download failed. Please try using the Print option instead.');
    console.error('Download error:', err);
  }}
}}

function saveToLocalStorage() {{
  try {{
    const state = {{
      currentQuestion,
      answers,
      bookmarks: Array.from(bookmarks),
      timerSeconds,
      timestamp: Date.now()
    }};
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }} catch (err) {{
    console.error('Save error:', err);
  }}
}}

function loadFromLocalStorage() {{
  try {{
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {{
      const state = JSON.parse(saved);
      const hasProgress = (state && (
        (state.currentQuestion && state.currentQuestion > 0) ||
        (state.answers && Object.keys(state.answers).length > 0) ||
        (state.timerSeconds && state.timerSeconds > 0)
      ));
      if (hasProgress && (Date.now() - state.timestamp < 24 * 60 * 60 * 1000)) {{
        if (confirm('Resume previous quiz session?')) {{
          currentQuestion = state.currentQuestion || 0;
          answers = state.answers || {{}};
          bookmarks = new Set(state.bookmarks || []);
          timerSeconds = state.timerSeconds || 0;
          updateTimer();
          loadQuestion(currentQuestion);
        }}
      }} else {{
        clearLocalStorage();
      }}
    }}
  }} catch (err) {{
    console.error('Load error:', err);
    clearLocalStorage();
  }}
}}

function clearLocalStorage() {{
  try {{
    localStorage.removeItem(STORAGE_KEY);
  }} catch (err) {{
    console.error('Clear storage error:', err);
  }}
}}

window.addEventListener('beforeunload', (e) => {{
  const resultSection = document.getElementById('resultSection');
  if (resultSection && !resultSection.classList.contains('hidden')) {{
    return;
  }}
  e.preventDefault();
  e.returnValue = '';
}});

window.addEventListener('unload', () => {{
  if (timerInterval) {{
    clearInterval(timerInterval);
  }}
}});
</script>
</body>
</html>
"""
    FileName = name.replace('/', '-').replace('|', ' ') + ".html"
    with open(FileName, "w", encoding="utf-8") as f:
        f.write(html)
    return FileName



# if __name__ == "__main__":
#   import requests, asyncio, base64
#   from urllib.parse import unquote_plus

#   resp = requests.get('https://u1.oliveboard.in/exams/solution/?c=rbip1sec&u=b27c55ac5886a360bf874356c39c8383_12754001053_312c66cf3069&m=1&testid=1')
#   NewData = []
#   DATA = resp.json()
#   NQs = DATA['settings']['nq']
#   positive_marking = DATA['settings']['cwmap'][0]
#   negative_marking = DATA['settings']['cwmap'][1].replace('-', '')
#   Time = str(int(DATA['settings']['tt'].replace(' Hours', '').replace(' Mins', ''))*60)
#   for item in DATA['sections']:
#     for idx, data in enumerate(DATA['sections'][f'{item}'], 1):
#       Ques = unquote_plus(data[1][0])
#       option1 = unquote_plus(data[2][0][0])
#       option2 = unquote_plus(data[2][1][0])
#       option3 = unquote_plus(data[2][2][0])
#       option4 = unquote_plus(data[2][3][0])
#       option5 = unquote_plus(data[2][4][0])
#       answer = data[6][0]
#       solution_text = unquote_plus(data[6][1])
#       NewData.append({"sr_no": idx, "question": decodeBase64(Ques), "option_1": decodeBase64(option1), "option_2": decodeBase64(option2), "option_3": decodeBase64(option3), "option_4": decodeBase64(option4), "option_5": decodeBase64(option5), "answer": answer, "negative_marking": negative_marking, "positive_marking": positive_marking, "solution_heading": "Full Solution", "solution_text": decodeBase64(solution_text)})
#   print(f"Total questions: {NQs}", Time, type(Time))
#   asyncio.run(generate_Mock_HTML(DATA["qpid"], Time, str(int(NQs)*int(positive_marking)), NQs, NewData))