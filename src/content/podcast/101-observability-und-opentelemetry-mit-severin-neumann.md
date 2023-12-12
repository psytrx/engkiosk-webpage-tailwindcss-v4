---
amazon_music: https://music.amazon.com/podcasts/c35a09fe-4116-4e04-8f68-77d61b112e46/episodes/72510b99-a2b0-4fca-8ecd-a3969347c78f/engineering-kiosk-101-observability-und-opentelemetry-mit-severin-neumann
apple_podcasts: https://podcasts.apple.com/us/podcast/101-observability-und-opentelemetry-mit-severin-neumann/id1603082924?i=1000638267638&uo=4
audio: https://audio1.redcircle.com/episodes/627265ce-6d39-4cc5-a9af-c1c3a3b68095/stream.mp3
chapter:
- start: 00:00:00
  title: Intro
- start: 00:01:07
  title: Unser Gast Severin Neumann, Sales Engineering und Demo Monkey
- start: 00:06:50
  title: Was ist Observability und wie unterscheidet es sich von Monitoring?
- start: 00:06:54
  title: 'About You: (Lead) DevOps/DataOps Engineer Google Cloud Platform (Werbung)'
- start: 00:07:56
  title: Was ist Observability und wie unterscheidet es sich von Monitoring?
- start: 00:15:24
  title: 'Signale bei Observability: Metrics, Logs und Traces'
- start: 00:17:25
  title: Was ist OpenTelemetry?
- start: 00:25:59
  title: APM-Anbieter und der Lock-in-Effekt
- start: 00:28:38
  title: OpenTelemetry als offener Standard
- start: 00:35:38
  title: Die Sicht von Dev und Ops auf OpenTelemetry
- start: 00:41:11
  title: Wie binde ich OpenTelemetry in meine App ein?
- start: 00:48:02
  title: Auto-Instrumentation, Microservice-Architektur und Trace-Headers
- start: 00:51:03
  title: Overhead beim Erheben von Daten und eigene Metadaten in Traces
- start: 00:56:12
  title: Speicherung von Observability-Daten
- start: 01:00:55
  title: Pitfalls und die Shortcomings von OpenTelemetry
- start: 01:05:26
  title: OpenTelemetry-Dokumentation
deezer: https://www.deezer.com/episode/584273752
description: "Effektive Observability mit OpenTelemetry Fr\xFCher waren viele Applikationen\
  \ eine Black Box, besonders f\xFCr die Ops aka Betriebsabteilung. Dann fing das\
  \ Logging an. Apps haben Log-Lines geschrieben, zum Beispiel wann die App fertig\
  \ hochgefahren ist oder wenn etwas schief gegangen ist. In einer Art und Weise haben\
  \ durch Logs die Devs angefangen, mit den Ops-Leuten zu kommunizieren. Irgendwann\
  \ sp\xE4ter gab es Metriken. Wie viel RAM verbraucht die App, wie oft wurde der\
  \ Garbage Collector getriggert oder auch Business-Metriken, wie oft eine Bestellung\
  \ ausgef\xFChrt wurde oder wann eine Geo- anstatt einer Text-Suche gestartet wurde.\
  \ War das alles? Nein. Der neueste Hype: Traces. Eine genaue Einsicht, welchen Code-Path\
  \ die App genommen hat und wie lange dieser gedauert hat inkl. aller Metadaten,\
  \ die wir uns w\xFCnschen. Und wenn man dies nun alles in einen Sack packt, es gut\
  \ durchsch\xFCttelt und man ein System hat, das man auf Basis dieser Daten fragen\
  \ stellen kann, nennt man das Observability. Und genau da setzt das Projekt OpenTelemetry\
  \ an. In dieser Episode sprechen wir mit dem Experten Severin Neumann \xFCber Observability\
  \ und OpenTelemetry. Bonus: Was ist ein Sales-Engineer?  **** Diese Episode wird\
  \ gesponsert von www.aboutyou.de  ABOUT YOU geh\xF6rt zu den gr\xF6\xDFten Online-Fashion\
  \ Shops in Europa und ist immer auf der Suche nach Tech-Talenten - wie zum Beispiel\
  \ einem (Lead) DevOps/DataOps Engineer Google Cloud Platform oder einem Lead Platform\
  \ Engineer. Alle Stellen findest auch unter https://corporate.aboutyou.de/en/our-jobs\_\
  \ ****  Das schnelle Feedback zur Episode: \U0001F44D (top)\_ \U0001F44E (geht so)"
google_podcasts: https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5yZWRjaXJjbGUuY29tLzBlY2ZkZmQ3LWZkYTEtNGMzZC05NTE1LTQ3NjcyN2Y5ZGY1ZQ/episode/YmIxYWY4MjktZTk4Mi00Zjk2LTkyODEtYjJiYjdiZGI3MWNi?sa=X&ved=2ahUKEwjJ0JyjtYmDAxUfNGIAHQllCZMQkfYCegQIARAF
headlines: links::Links||sprungmarken::Sprungmarken||hosts::Hosts||feedback-gerne-auch-als-voice-message::Feedback
  (gerne auch als Voice Message)
image: ./101-observability-und-opentelemetry-mit-severin-neumann.jpg
length_second: 4153
pubDate: 2023-12-12 05:00:00+00:00
rtlplus: ''
speaker:
- name: Andy Grunwald
  transcriptLetter: A
  website: https://andygrunwald.com/
- name: Wolfi Gassler
  transcriptLetter: B
  website: https://wolfgang.gassler.org/
- name: Severin Neumann
  transcriptLetter: C
  website: https://www.linkedin.com/in/severinneumann/
spotify: https://open.spotify.com/episode/1RkWRmsfnRMBfDrYKNGDRf
tags:
- DevOps
- Software Engineering
- Interview
title: '#101 Observability und OpenTelemetry mit Severin Neumann'
youtube: ''

---
<p><span>Effektive Observability mit OpenTelemetry</span></p><p><span>Früher waren viele Applikationen eine Black Box, besonders für die Ops aka Betriebsabteilung. Dann fing das Logging an. Apps haben Log-Lines geschrieben, zum Beispiel wann die App fertig hochgefahren ist oder wenn etwas schief gegangen ist. In einer Art und Weise haben durch Logs die Devs angefangen, mit den Ops-Leuten zu kommunizieren.</span></p><p><span>Irgendwann später gab es Metriken. Wie viel RAM verbraucht die App, wie oft wurde der Garbage Collector getriggert oder auch Business-Metriken, wie oft eine Bestellung ausgeführt wurde oder wann eine Geo- anstatt einer Text-Suche gestartet wurde.</span></p><p><span>War das alles? Nein. Der neueste Hype: Traces. Eine genaue Einsicht, welchen Code-Path die App genommen hat und wie lange dieser gedauert hat inkl. aller Metadaten, die wir uns wünschen.</span></p><p><span>Und wenn man dies nun alles in einen Sack packt, es gut durchschüttelt und man ein System hat, das man auf Basis dieser Daten fragen stellen kann, nennt man das Observability.</span></p><p><span>Und genau da setzt das Projekt OpenTelemetry an.</span></p><p><span>In dieser Episode sprechen wir mit dem Experten Severin Neumann über Observability und OpenTelemetry.</span></p><p><span>Bonus: Was ist ein Sales-Engineer?</span></p><p><br></p><p><span>**** Diese Episode wird gesponsert von </span><a href="https://www.aboutyou.de" rel="nofollow">www.aboutyou.de</a><span> </span></p><p><span>ABOUT YOU gehört zu den größten Online-Fashion Shops in Europa und ist immer auf der Suche nach Tech-Talenten - wie zum Beispiel einem </span><a href="https://corporate.aboutyou.de/en/jobs/team-lead-tech-gcp-operations?trid=599daa44-acdb-4457-98c9-0d911d8cd9ab&utm_campaign=tech_gcp_operations&utm_medium=podcast&utm_source=engineering_kiosk" rel="nofollow">(Lead) DevOps/DataOps Engineer Google Cloud Platform</a><span> oder einem </span><a href="https://corporate.aboutyou.de/en/jobs/lead-platform-engineer-m-f-d?trid=599daa44-acdb-4457-98c9-0d911d8cd9ab&utm_campaign=lead_platform_engineer&utm_medium=podcast&utm_source=engineering_kiosk" rel="nofollow">Lead Platform Engineer</a><span>. Alle Stellen findest auch unter </span><a href="https://corporate.aboutyou.de/en/our-jobs" rel="nofollow">https://corporate.aboutyou.de/en/our-jobs</a><span> </span></p><p><span>****</span></p><p><br></p><p><strong>Das schnelle Feedback zur Episode:</strong></p><p><a href="https://api.openpodcast.dev/feedback/101/upvote" rel="nofollow"><strong>👍 (top)</strong></a><strong>  </strong><a href="https://api.openpodcast.dev/feedback/101/downvote" rel="nofollow"><strong>👎 (geht so)</strong></a></p><p><br></p><p><span>Feedback (gerne auch als Voice Message)</span></p><ul><li><span>EngKiosk Community: </span><a href="https://engineeringkiosk.dev/join-discord">https://engineeringkiosk.dev/join-discord</a><span> </span></li><li><span>Email: </span><a href="mailto:stehtisch@engineeringkiosk.dev" rel="nofollow">stehtisch@engineeringkiosk.dev</a></li><li><span>Mastodon: </span><a href="https://podcasts.social/@engkiosk" rel="nofollow">https://podcasts.social/@engkiosk</a></li><li><span>Twitter: </span><a href="https://twitter.com/EngKiosk" rel="nofollow">https://twitter.com/EngKiosk</a></li><li><span>WhatsApp </span>+49 15678 136776</li></ul><p><br></p><p><span>Gerne behandeln wir auch euer Audio Feedback in einer der nächsten Episoden, einfach Audiodatei per </span><a href="https://engineeringkiosk.dev/kontakt/">Email</a><span> oder WhatsApp Voice Message an </span>+49 15678 136776</p><p><br></p><h3 id="links">Links</h3><ul><li><span>Severin Neumann: </span><a href="https://www.linkedin.com/in/severinneumann/" rel="nofollow">https://www.linkedin.com/in/severinneumann/</a></li><li><span>DemoMonkey: </span><a href="https://github.com/svrnm/DemoMonkey" rel="nofollow">https://github.com/svrnm/DemoMonkey</a></li><li><span>OpenTelemetry: </span><a href="https://opentelemetry.io/" rel="nofollow">https://opentelemetry.io/</a></li><li><span>OpenTracing: </span><a href="https://opentracing.io/" rel="nofollow">https://opentracing.io/</a></li><li><span>W3C Trace Context: </span><a href="https://www.w3.org/TR/trace-context/" rel="nofollow">https://www.w3.org/TR/trace-context/</a></li><li><span>W3C Trace Context: AMQP protocol: </span><a href="https://w3c.github.io/trace-context-amqp/" rel="nofollow">https://w3c.github.io/trace-context-amqp/</a></li><li><span>OpenTelemetry Vendors: </span><a href="https://opentelemetry.io/ecosystem/vendors/" rel="nofollow">https://opentelemetry.io/ecosystem/vendors/</a></li><li><span>OpenTelemetry Instrumentation: </span><a href="https://opentelemetry.io/docs/instrumentation/" rel="nofollow">https://opentelemetry.io/docs/instrumentation/</a></li><li><span>Dynatrace: </span><a href="https://www.dynatrace.com/de/" rel="nofollow">https://www.dynatrace.com/de/</a></li><li><span>AppDynamics: </span><a href="https://www.appdynamics.com/" rel="nofollow">https://www.appdynamics.com/</a></li><li><span>OpenTelemetry Tracing for Monoliths - Phillip Carter, Honeycomb: </span><a href="https://www.youtube.com/watch?v=kzXT0WlTBpw" rel="nofollow">https://www.youtube.com/watch?v=kzXT0WlTBpw</a></li></ul><p><br></p><h3 id="sprungmarken">Sprungmarken</h3><p><span>(00:00:00) Intro</span></p><p><span>(00:01:07) Unser Gast Severin Neumann, Sales Engineering und Demo Monkey</span></p><p><span>(00:06:50) Was ist Observability und wie unterscheidet es sich von Monitoring?</span></p><p><span>(00:06:54) About You: (Lead) DevOps/DataOps Engineer Google Cloud Platform (Werbung)</span></p><p><span>(00:07:56) Was ist Observability und wie unterscheidet es sich von Monitoring?</span></p><p><span>(00:15:24) Signale bei Observability: Metrics, Logs und Traces</span></p><p><span>(00:17:25) Was ist OpenTelemetry?</span></p><p><span>(00:25:59) APM-Anbieter und der Lock-in-Effekt</span></p><p><span>(00:28:38) OpenTelemetry als offener Standard</span></p><p><span>(00:35:38) Die Sicht von Dev und Ops auf OpenTelemetry</span></p><p><span>(00:41:11) Wie binde ich OpenTelemetry in meine App ein?</span></p><p><span>(00:48:02) Auto-Instrumentation, Microservice-Architektur und Trace-Headers</span></p><p><span>(00:51:03) Overhead beim Erheben von Daten und eigene Metadaten in Traces</span></p><p><span>(00:56:12) Speicherung von Observability-Daten</span></p><p><span>(01:00:55) Pitfalls und die Shortcomings von OpenTelemetry</span></p><p><span>(01:05:26) OpenTelemetry-Dokumentation</span></p><p><br></p><h3 id="hosts">Hosts</h3><ul><li><span>Wolfgang Gassler (</span><a href="https://mastodon.social/@woolf" rel="nofollow">https://mastodon.social/@woolf</a><span>)</span></li><li><span>Andy Grunwald (</span><a href="https://twitter.com/andygrunwald" rel="nofollow">https://twitter.com/andygrunwald</a><span>)</span></li></ul><p><br></p><h3 id="feedback-gerne-auch-als-voice-message">Feedback (gerne auch als Voice Message)</h3><ul><li><span>EngKiosk Community: </span><a href="https://engineeringkiosk.dev/join-discord">https://engineeringkiosk.dev/join-discord</a><span> </span></li><li><span>Email: </span><a href="mailto:stehtisch@engineeringkiosk.dev" rel="nofollow">stehtisch@engineeringkiosk.dev</a></li><li><span>Mastodon: </span><a href="https://podcasts.social/@engkiosk" rel="nofollow">https://podcasts.social/@engkiosk</a></li><li><span>Twitter: </span><a href="https://twitter.com/EngKiosk" rel="nofollow">https://twitter.com/EngKiosk</a></li><li><span>WhatsApp </span>+49 15678 136776</li></ul>