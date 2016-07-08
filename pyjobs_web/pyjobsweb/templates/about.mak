## -*- coding: utf-8 -*-
<%inherit file="local:templates.master"/>

<%def name="title()">
    pyjobs — à propos
</%def>

<header class="page-header">
    <div class="container">
        <h1>pyjobs est développé par la société <a href="http://algoo.fr">algoo</a></h1>
    </div>
</header>

<div class="container">
    <h2>algoo &mdash; spécialiste du développement d'applications web et SAAS</h2>
    <p>
        Nous sommes une jeune startup grenobloise spécialisée dans le développement d'applications web en python.
    </p>
    <p>
        Nous intervenons sur des points spécifiques de vos projets (mise en place de géolocalisation, paiement en
        ligne, crawling, moteurs de recherche, interconnections d'api, ...) ou prenons les projets dans leur intégralité
        et livrons des solutions opérationnelles «&nbsp;clé-en-main&nbsp;».
    </p>
    <p>
        <a href="http://algoo.fr">Nous vous invitons à découvrir nos compétences et à nous contacter si vous voulez en savoir plus</a>
    </p>
    <h2>pyjobs &mdash; mise en relation de candidats et recruteurs «&nbsp;python&nbsp;»</h2>
    <p>
        pyjobs est né d'un constat simple&nbsp;: il manque un lien entre développeurs et recruteurs python.
        Lorsqu'on est développeur, il n'est pas évident de trouver des annonces intéressantes proposant du travail en
        python car beaucoup de sociétés sont peu visibles. Lorsqu'on est recruteur, on a peu de candidats car les
        compétences sont à chercher sur différents job-boards, ce qui multiplie les démarches et le coût en temps.
    </p>
    <p>
        pyjobs est un service basé sur des logiciels libres et totalement réutilisables. Vous trouverez
        <a href="https://github.com/pyjobs/">toutes les ressources nécessaires sur les dépôts github</a>.
    </p>
    <p>
        Pour toute remarque ou question, n'hésitez pas à
        <a id="mailto" href="">nous contacter</a>
        voire à parler de nous :)
    </p>
</div>

<%def name="end_body_scripts()">
    <script type="text/javascript">
        decodeBase64 = function(s) {
            var e={},i,b=0,c,x,l=0,a,r='',w=String.fromCharCode,L=s.length;
            var A="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
            for(i=0;i<64;i++){e[A.charAt(i)]=i;}
            for(x=0;x<L;x++){
                c=e[s.charAt(x)];b=(b<<6)+c;l+=6;
                while(l>=8){((a=(b>>>(l-=8))&0xff)||(x<(L-2)))&&(r+=w(a));}
            }
            return r;
        };

        // Set email on link (email base64 encoded for robots)
        document.getElementById('mailto').href = 'mailto:' +  decodeBase64('Y29udGFjdEBhbGdvby5mcg==') + '?subject=pyjobs';
    </script>
</%def>
